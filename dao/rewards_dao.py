import json
from datetime import datetime, timezone
from typing import List

import requests

from dao.base_dao import BaseDao, DBResultError
from config import config
from models.metadata.metadata_models import EntityType, Source
from models.rewards.rewards_model import RewardStatus
from utils.get_random_string import get_random_string


class RewardsDao(BaseDao):
    def last_payout_info(self, public_address: str, status: list = []) -> any:
        query = {
            "selector": {
                "public_address": public_address,
                "status": {
                    "$in": status
                }
            },
            "limit": 1,
            "sort": [
                {
                    "updated_at": "desc"
                }
            ]
        }

        result = self.query_data(query)["result"]
        if len(result) == 0:
            return None

        return result[0]

    def create_new_claim(self, public_address: str, start_date: datetime, end_date: datetime,
                         source: Source, entity_type: EntityType = "") -> str:
        doc_id = get_random_string(15)
        create_time = datetime.now().replace(microsecond=0).isoformat()

        document = {
            'public_address': public_address,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'created_at': create_time,
            'entity_type': entity_type.name if entity_type else None,
            'status': RewardStatus.CREATED,
            'source': source
        }
        self.save(doc_id, document)
        return doc_id

    def update_claim_as_successful(self, claim_id: str, transaction_hash: str, entity_ids=List[str]) -> str:
        document = self.get_doc_by_id(doc_id=claim_id)

        document['transaction_hash'] = transaction_hash
        document['status'] = RewardStatus.TRANSFER_SUCCEEDED
        document['entity_ids'] = entity_ids
        self.update_claim(claim_id, document)

    def update_claim_to_transferring(self, claim_id: str, amount: int, contract_address: str, sender_address: str,
                                     entity_ids=List[str]):
        document = self.get_doc_by_id(doc_id=claim_id)
        document['amount'] = amount
        document['contract_address'] = contract_address
        document['sender_address'] = sender_address
        document['status'] = RewardStatus.TRANSFERRING
        document["entity_ids"] = entity_ids
        self.update_claim(claim_id, document)

    def update_claim_to_failed(self, claim_id: str, reason: str):
        document = self.get_doc_by_id(doc_id=claim_id)
        document['status'] = RewardStatus.FAILED
        document['reason'] = reason
        self.update_claim(claim_id, document)

    def get_rewards_list(self, public_address: str, entity_type: EntityType, page: int):
        query = {
            "selector": {
                "public_address": public_address,
                "entity_type": entity_type
            },
            "limit": self.page_size,
            "skip": (page - 1) * self.page_size,
            "sort": [
                {
                    "created_at": "desc"
                }
            ]
        }

        result = self.query_data(query)["result"]
        return result
    
    def get_total_earning_list(self, public_address: str, source: Source):
        query = {
            "selector": {
                "public_address": public_address,
                "source": source,
                "status": RewardStatus.TRANSFER_SUCCEEDED
            },
            "sort": [
                {
                    "created_at": "desc"
                }
            ],
            "fields": ["_id", "public_address", "start_date", "end_date", "amount"]
        }

        result = self.query_data(query)["result"]
        return result

    def is_claim_in_progress(self, public_address: str, source: Source, entity_type: EntityType):
        query = {
            "selector": {
                "public_address": public_address,
                "entity_type": entity_type,
                "source": source,
                "status": {"$in": [RewardStatus.CREATED, RewardStatus.TRANSFERRING, RewardStatus.CALCULATING]}
            },
            "limit": 1,
            "skip": 0,
            "sort": [
                {
                    "created_at": "desc"
                }
            ]
        }

        result = self.query_data(query)["result"]
        return len(result) == 1

    def is_one_time_reward_claimed(self, public_address: str, source: Source, entity_type: str):
        query = {
            "selector": {
                "public_address": public_address,
                "entity_type": entity_type,
                "source": source,
                "status": {"$in": [RewardStatus.TRANSFER_SUCCEEDED]}
            },
            "limit": 1,
            "skip": 0,
            "sort": [
                {
                    "created_at": "desc"
                }
            ]
        }

        result = self.query_data(query)["result"]
        return len(result) >= 1

    def update_claim(self, claim_id: str, document: dict):
        document['updated_at'] = datetime.now().replace(microsecond=0).isoformat()
        self.update_doc(doc_id=claim_id, data=document)

    def get_claim_count(self, date: datetime, source: Source, public_address: str) -> int:
        key = f"[\"{public_address}\",\"{source}\",{date.year}, {date.month}, {date.day}]"
        query_url = f"/_design/successful-claims-per-day/_view/successful-claims-per-day?key={key}&" \
                    f"reduce=true&group_level=5"
        url = "http://{0}:{1}@{2}/{3}/{4}".format(
            self.user, self.password, self.db_host, self.db_name, query_url
        )
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise DBResultError(self.db_name, response.text)
        data = json.loads(response.text)["rows"]
        if len(data) == 0:
            return 0

        return data[0]["value"]

    def save_record_from_blockchain(self, sender: str, receiver: str, amount: int, block_number: str,
                                    network_name: str, transaction_hash: str, entity_type: EntityType):
        doc_id = get_random_string(15)
        create_time = datetime.now().replace(microsecond=0).isoformat()

        document = {
            'public_address': receiver,
            'sender': sender,
            'block_number': block_number,
            'network_name': network_name,
            'created_at': create_time,
            'entity_type': entity_type,
            'status': RewardStatus.TRANSFER_SUCCEEDED,
            'source': "blockchain",
            'amount': amount,
            'transaction_hash': transaction_hash
        }
        self.save(doc_id, document)
        return doc_id

    def is_transaction_already_saved(self, transaction_hash: str):
        query = {
            "selector": {
                "transaction_hash": transaction_hash
            },
            "limit": 1,
            "skip": 0
        }

        result = self.query_data(query)["result"]
        return len(result) == 1

    def get_total_rewards(self, public_address: str) -> int:
        start_key = f"[\"{public_address}\"]"
        end_key = f"[\"{public_address}\",{{}}]"

        query_url = f"_design/payouts/_view/payouts?start_key={start_key}&end_key={end_key}&" \
                    f"reduce=true&group_level=1"
        url = "http://{0}:{1}@{2}/{3}/{4}".format(
            self.user, self.password, self.db_host, self.db_name, query_url
        )
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise DBResultError(self.db_name, response.text)
        data = json.loads(response.text)["rows"]
        if len(data) == 0:
            return 0

        return data[0]["value"]

    def get_earning_over_time(self, public_address: str, start_date:str , end_date: str):
        start_key = f"[\"{public_address}\",\"{start_date}\"]"
        end_key = f"[\"{public_address}\",\"{end_date}\"]"
        query_url = f"/_design/payouts/_view/get-earning?start_key={start_key}&end_key={end_key}"
        url = "http://{0}:{1}@{2}/{3}/{4}".format(
            self.user, self.password, self.db_host, self.db_name, query_url
        )
        headers = {"Content-Type": "application/json"}
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise DBResultError(self.db_name, response.text)
        data = json.loads(response.text)
        if len(data["rows"]) == 0:
            return 0
        return data["rows"][0]["value"]

rewards_dao = RewardsDao()
rewards_dao.set_config(
    config["couchdb"]["user"],
    config["couchdb"]["password"],
    config["couchdb"]["db_host"],
    config["couchdb"]["rewards_db"],
)
