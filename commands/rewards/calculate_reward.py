from typing import List

from commands.base_command import BaseCommand
from commands.metadata.create_new_entity.create_brainstem_entity import EntitySubType
from dao.metadata_dao import image_metadata_dao
from dao.rewards_dao import rewards_dao
from dao.users_dao import user_dao
from models.metadata.metadata_models import EntityType, Source, EntityRewardStatus
from datetime import datetime, timedelta
from dateutil import parser
from models.rewards.rewards_model import RewardStatus
from web3 import Web3
from config import config

class CalculateRewardCommand(BaseCommand):

    def __init__(self, public_address: str, source: Source, entity_type: EntityType, end_date_delta: int = 1):
        super(CalculateRewardCommand, self).__init__(public_address)
        self.entity_type = entity_type

        self.upload_reward = 0.1
        self.tag_annotations_reward = 0.1
        self.text_annotations_reward = 0.1
        self.verifications_rewards = 0.1
        self.default_start_date = datetime.strptime('1-1-2021', '%d-%m-%Y')
        self.end_date = datetime.utcnow().today() - timedelta(days=end_date_delta)
        self.source = source
        self.end_date_delta = end_date_delta

    def execute(self):
        if self.source == Source.wedatanation:
            self.successful = True
            amount, entity_ids = self.calculate_wedatanation_reward()
            return {'amount': amount, "app": self.source, "entity_ids": entity_ids}

        if self.source == Source.recyclium:
            self.successful = True
            user = user_dao.get_by_public_address(self.public_address)['result'][0]
            return {'amount': user['rewards'], 'app': self.source, 'entity_ids': []}

        claim_start_date = self.get_claim_start_date()

        if claim_start_date.date() == datetime.utcnow().date() and self.end_date_delta == 1:
            self.successful = False
            self.messages.append("Claim start date cannot be today.")
            return

        amount = self.calculate_amount_in_wei(claim_start_date)
        self.successful = True
        format_code = "%d-%m-%Y"
        return {'amount': amount, 'start_date': claim_start_date.strftime(format_code),
                'end_date': self.end_date.strftime(format_code), "app": self.source}

    def calculate_amount_in_wei(self, start_date: datetime = None) -> int:
        if start_date is None:
            start_date = self.default_start_date

        if self.source == Source.brainstem:
            amount = self.calculate_brainstem_reward(start_date)
        else:
            result = image_metadata_dao.get_user_stats_count(self.public_address, self.entity_type, start_date,
                                                             self.end_date)

            amount = self.upload_reward * result['uploads'] + self.tag_annotations_reward * result[
                'tag_annotations'] + self.text_annotations_reward * result[
                         'text_annotations'] + self.verifications_rewards * result[
                         'verifications']
            amount = int(amount * 10 ** 18)
        return amount

    def get_claim_start_date(self) -> datetime:

        status_list = [RewardStatus.CREATED, RewardStatus.TRANSFERRING, RewardStatus.TRANSFER_SUCCEEDED]
        last_payout_info = rewards_dao.last_payout_info(self.public_address, status_list)

        if last_payout_info is None:
            return self.default_start_date
        last_payout_end_date = parser.parse(last_payout_info['end_date'])
        return last_payout_end_date + timedelta(days=1)
    
    def calculate_litterbux_reward(self)->(int, List[str]):
        amount = 0
        entity_ids = []
        if self.entity_type == EntityType.tutorial:
            if user_dao.get_tutorial_reward_status(self.public_address) != EntityRewardStatus.unpaid:
                amount = config["application"].getint("reward_start_tutorial", 10)
 
        if self.entity_type == EntityType.referral:
            claimables = user_dao.get_claimable_referral_rewards(self.public_address)
            for claim in claimables:
                entity_ids.append(claim["_id"])
            amount = len(claimables) * config["application"].getint("reward_referral", 10)
 
        if self.entity_type == EntityType.image:
            start_key = f'["{self.public_address}"]'
            end_key = f'["{self.public_address}",{{}}]'
            result = image_metadata_dao.query_view_by_key_range("reward-status", "litterbux_claimable_uploads", start_key, end_key, 0)
            amount = len(result['rows']) * config["application"].getint("reward_upload", 1)
            for row in result['rows']:
                value = row["value"]
                entity_ids.append(value["id"])
        
        return  Web3.toWei(amount, 'ether'), entity_ids

    def calculate_litterbux_reward_status(self):
        result = []
        if user_dao.get_tutorial_reward_status(self.public_address) != None:
            result.append({
                'type': 'tutorial',
                'reward': config["application"].getint("reward_start_tutorial", 10),
                'reward_status': user_dao.get_tutorial_reward_status(self.public_address)
            })
        
        referred_users = user_dao.get_referral_rewards_status(self.public_address)
        if referred_users != None:
            for referred_user in referred_users:
                result.append({
                    'type': 'referral',
                    'reward': config["application"].getint("reward_referral", 10),
                    'reward_status': referred_user["referral_reward_status"]
                })

        keys = []
        keys.append(f"\"{self.public_address}\"")

        upload_result = image_metadata_dao.query_view_by_keys("reward-status", "litterbux", keys)
        for row in upload_result['rows']:
            value = row["value"]
            result.append({
                'type': 'upload',
                'reward': config["application"].getint("reward_upload", 1),
                'reward_status': value["reward_status"]
            })
        
        return result
            
    
    def update_litterbux_reward(self, entity_ids):
        if self.entity_type == EntityType.tutorial:
            user_dao.set_tutorial_reward_claimed(self.public_address, EntityRewardStatus.paid)

        if self.entity_type == EntityType.referral:
            user_dao.set_referral_rewards_claimed(self.public_address)

        if self.entity_type == EntityType.image:
            for entity_id in entity_ids:
                parent_doc = image_metadata_dao.get_doc_by_id(entity_id)
                parent_doc["reward_status"] = EntityRewardStatus.paid
                image_metadata_dao.update_doc(doc_id=parent_doc["_id"], data=parent_doc)

 
    def calculate_wedatanation_reward(self) -> (int, List[str]):

        rewards_dict = {
            # Dict keys 0 = 1st upload, 1st index = 2nd upload and so on.
            "upload": {
                0: 2.5,
                1: 1.25,
                2: 1.5,
                3: 1.75,
                4: 2,
                5: 2.25
            }
        }

        start_key = f'["{self.public_address}"]'
        end_key = f'["{self.public_address}",{{}}]'

        result = image_metadata_dao.query_view_by_key_range("reward-status", "wedatanation", start_key, end_key, 0)

        amount = 0
        entity_ids = []
        for row in result['rows']:
            value = row["value"]
            if value["type"] == "upload":
                amount += rewards_dict["upload"].get(value["count"], 0)
                entity_ids.append(row["value"]["id"])
        amount = Web3.toWei(amount, 'ether')
        return amount, entity_ids

    def calculate_brainstem_reward(self, start_date: datetime) -> int:

        rewards_dict = {
            EntitySubType.hbr_rr: 1,
            EntitySubType.user_metadata: 1,
            EntitySubType.summary: 1,
            EntitySubType.over_chunk: 1
        }

        start_key = f'["{self.public_address}",{start_date.year},{start_date.month},{start_date.day}]'
        end_key = (
            f'["{self.public_address}",{self.end_date.year},{self.end_date.month},{self.end_date.day},{{}}]'
        )
        result = image_metadata_dao.query_view_by_key_range("reward-status", "brainstem", start_key, end_key, 0)
        amount = 0
        for row in result['rows']:
            value = row["value"]
            amount += rewards_dict[value["type"]]
        amount = Web3.toWei(amount, 'ether')
        return amount


class CannotClaimRewardException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
