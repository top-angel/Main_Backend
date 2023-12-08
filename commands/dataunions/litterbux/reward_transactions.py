import time
import logging
import sys
import os
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler

from commands.base_command import BaseCommand
from commands.dataunions.ncights.rank_users_command import RankUserCommand
from commands.dataunions.litterbux.add_rewards_command import AddRewardsCommand
from config import config
from dao.others_dao import others_db, NotificationType
from dao.users_dao import user_dao
from dao.metadata_dao import image_metadata_dao
from dao.rewards_dao import rewards_dao
from commands.rewards.calculate_reward import CalculateRewardCommand, CannotClaimRewardException

from models.metadata.metadata_models import Source, EntityType, EntityRewardStatus
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_account.signers.local import LocalAccount
from utils.get_project_dir import get_project_root
from utils.abi.erc20_abi import ERC20_ABI
from models.rewards.rewards_model import ClaimRewardErrorMessages, RewardStatus
from requests import HTTPError
from dao.base_dao import DBResultError


log_filename = os.path.join(get_project_root(), 'logs', "litterbux_reward_allocation_task.log")
handler = TimedRotatingFileHandler(filename=log_filename, when="D", interval=1)

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=config["logging"].getint("level"),
    handlers=[handler],
)


def my_handler(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))


# Install exception handler
sys.excepthook = my_handler
    

class UserReferralInfo:
  def __init__(self, public_address:str, raw_earning: float, referred_users: list, referral_id: str, entity_ids: list):
    self.public_address = public_address
    self.earnings = 0
    self.raw_earnings = raw_earning
    self.referred_users = referred_users
    self.referral_id = referral_id
    self.entity_ids = entity_ids

class RewardTransactions(BaseCommand):
  def __init__(self):
    self.users = {}
    self.ref_calc_infos = {}
    self.litterbux_referral_bonus_starting_percent = config["application"].getfloat("litterbux_referral_bonus_starting_percent", 10)
    super(RewardTransactions, self).__init__()

  def execute(self):
    logging.debug("Executing notification generation task")
    all_users = user_dao.get_all()["result"]
    self.users = all_users
    for user in all_users:
      
      # get claimable rewards
      public_address = user["public_address"]
      amount, entity_ids = self.calculate_litterbux_claimable_rewards(public_address)
      
      referred_users = user.get("referred_users", [])
      referral_id = user.get("referral_id", "") or ""
      self.ref_calc_infos[public_address] = UserReferralInfo(public_address, amount, referred_users, referral_id, entity_ids)
    
    for user in self.ref_calc_infos.values():
      public_address = user.public_address
      self.ref_calc_infos[public_address].earnings = self._recursive_earnings(user, 0, 1)
      amount = self.ref_calc_infos[public_address].earnings + user.raw_earnings
      
      add_rewards_c = AddRewardsCommand(public_address, self.ref_calc_infos[public_address].earnings)
      add_rewards_c.execute()

      
      print("reward status: ", public_address, user.raw_earnings, user.earnings)
      user.entity_ids.append({'type': 'rewards_pyramid', 'id': ''})
      entity_ids = user.entity_ids
      amount = Web3.toWei(amount, 'ether')
      
      claim_id = None
      if amount != 0:
        try:
          start_date = datetime.now()
          claim_id = rewards_dao.create_new_claim(public_address, start_date, start_date,
                                                  Source.litterbux, EntityType.image)

          sender_address = Account.from_key(config["rewards"]["account_private_key"]).address
          rewards_dao.update_claim_to_transferring(claim_id, amount, config["rewards"]["litterbux_token_address"],
                                                    sender_address, entity_ids=entity_ids)
          # transfer rewards
          transaction_hash = self.transfer(public_address, amount)

          rewards_dao.update_claim_as_successful(claim_id, transaction_hash, entity_ids=entity_ids)
          logging.debug("Reward transfer transaction for user [%s]: [%s]", public_address, transaction_hash)
          
          # update status
          self.update_litterbux_claim_status(public_address, entity_ids)
        
        except HTTPError as err:
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except DBResultError as err:
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except CannotClaimRewardException as err:
            rewards_dao.update_claim_to_failed(claim_id, str(err))

        except ContractLogicError as err:
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except Exception as err:
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)
      
    self.successful = True 
    logging.info("Finished generating notifications")

  def transfer(self, public_address:str, amount: int) -> str:
        # Constants
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        token_contract_address = Web3.toChecksumAddress(config["rewards"]["litterbux_token_address"])
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)
        contract = web3.eth.contract(address=token_contract_address, abi=ERC20_ABI)
        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(public_address), f"Not a valid address: {public_address}"

        txn = contract.functions.transfer(public_address, amount).buildTransaction({'nonce': nonce, 'chainId': chain_id, 'from': account.address})

        signed_txn = web3.eth.account.signTransaction(txn, private_key=sender_account_private_key)
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_hash = signed_txn.hash.hex()
        max_attempts = 3
        tx_receipt = None
        for i in range(max_attempts):
            time.sleep(5)
            logging.info("Attempt [%s] to get receipt for transaction [%s]", i, tx_hash)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt is not None:
                logging.info("Found tx_receipt [%s]", tx_receipt)
                break

        if tx_receipt is not None and tx_receipt['status'] != 1:
            raise CannotClaimRewardException(f"Transaction transaction receipt status [{tx_receipt['status']}]")
        tx_hash = signed_txn.hash.hex()
        return tx_hash
        
  def update_litterbux_claim_status(self, public_address: str, entity_ids: list):
    for entity_id in entity_ids:
      if entity_id["type"] == 'tutorial':
        user_dao.set_tutorial_reward_claimed(public_address, EntityRewardStatus.paid)

      if entity_id["type"] == 'referral':
        user_dao.set_referral_rewards_claimed(public_address)
      if entity_id["type"] == 'upload':
        parent_doc = image_metadata_dao.get_doc_by_id(entity_id["id"])
        parent_doc["reward_status"] = EntityRewardStatus.paid
        image_metadata_dao.update_doc(doc_id=parent_doc["_id"], data=parent_doc)

      
  def calculate_litterbux_claimable_rewards(self, public_address: str):
    amount = 0
    entity_ids = []
    
    tutorial_status = user_dao.get_tutorial_reward_status(public_address)
    if tutorial_status == EntityRewardStatus.unpaid:
      amount += config["application"].getint("reward_start_tutorial", 10)
      entity_ids.append({'type': 'tutorial', 'id': ''})

    claimables = user_dao.get_claimable_referral_rewards(public_address)
    for claim in claimables:
        entity_ids.append({'type': 'referral', 'id': claim["_id"]})
    amount += len(claimables) * config["application"].getint("reward_referral", 10)

    images = image_metadata_dao.query_view_by_keys("reward-status", "litterbux_claimable_uploads", [f"\"{public_address}\""])
    amount += len(images['rows']) * config["application"].getint("reward_upload", 1)
    for row in images['rows']:
        value = row["value"]
        entity_ids.append({'type': 'upload', 'id': value["id"]})
    return  amount, entity_ids
  
  def _recursive_earnings(self, user: UserReferralInfo, earning: float, level=1):
    # find referred users
    referred_users = user.referred_users

    for referred_user in referred_users:
      # find next tier referee
      for ref_calc_info in self.ref_calc_infos.values():
        if ref_calc_info.public_address == referred_user:
          percentage = (self.litterbux_referral_bonus_starting_percent * 2) / (2 ** level)
          if percentage > 0 :
            earning += ref_calc_info.raw_earnings * (percentage / 100)
            earning = self._recursive_earnings(ref_calc_info, earning,level+1)
          break
    return earning
  
  def calculate_litterbux_rewards_pyramid(self):
    for referral_info in self.ref_calc_infos.values():
      referral_info.earnings += self._recursive_earnings(referral_info, 0, 1)
      self.successful = True
  
  
if __name__ == "__main__":
    c = RewardTransactions()
    c.execute()
    assert c.successful

