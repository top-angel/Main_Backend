import time
from datetime import datetime

from eth_account import Account
from eth_account.signers.local import LocalAccount
from requests import HTTPError
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware

from commands.rewards.calculate_reward import CalculateRewardCommand, CannotClaimRewardException
from commands.base_command import BaseCommand
from config import config
from web3 import Web3, HTTPProvider
from dao.users_dao import user_dao
from dao.base_dao import DBResultError
from dao.metadata_dao import image_metadata_dao
from models.metadata.metadata_models import EntityType, Source, EntityRewardStatus
from dao.rewards_dao import rewards_dao
import logging

from models.rewards.rewards_model import ClaimRewardErrorMessages, RewardStatus
from utils.abi.erc20_abi import ERC20_ABI


class ClaimRewardCommand(CalculateRewardCommand):

    def __init__(self, public_address: str, source: Source, entity_type: EntityType = None, amount: str = None):
        super(ClaimRewardCommand, self).__init__(public_address, source, entity_type)
        self.public_address = public_address
        self.entity_type = entity_type
        self.validate_input()
        self.min_amount = 1
        self.amount = amount
        self.reward_config = {
            Source.wedatanation: {
                "max_daily_claims": 10,
                "minimum_amount": 1,
                "maximum_amount": 100 ** 18
            },
            Source.default: {
                "max_daily_claims": 1,
                "minimum_amount": 1,
                "maximum_amount": 100 ** 18
            },
            Source.brainstem: {
                "max_daily_claims": 1,
                "minimum_amount": 1,
                "maximum_amount": 100 ** 18
            },
            Source.ncight: {
                "max_daily_claims": 1,
                "minimum_amount": 1,
                "maximum_amount": 100 ** 18
            },
            Source.litterbux: {
                "max_daily_claims": 3,
                "minimum_amount": 1,
                "maximum_amount": 100 ** 18
            }
        }

    def execute(self):
        self.successful = False

        if rewards_dao.is_claim_in_progress(self.public_address, self.source, self.entity_type):
            self.messages.append(ClaimRewardErrorMessages.ALREADY_IN_PROGRESS)
            return

        max_claim_per_day = self.reward_config[self.source]["max_daily_claims"]
        if self.source != Source.litterbux and rewards_dao.get_claim_count(datetime.utcnow(), self.source, self.public_address) >= max_claim_per_day:
            self.messages.append(ClaimRewardErrorMessages.EXCEEDS_DAILY_LIMIT)
            return

        if self.source == Source.litterbux:
            amount = self.calculate_litterbux_reward()
            if amount == 0:
                self.messages.append(ClaimRewardErrorMessages.AMOUNT_TOO_SMALL)
                return
            

        start_date = self.get_claim_start_date()
        claim_id = rewards_dao.create_new_claim(self.public_address, start_date, self.end_date,
                                                self.source, self.entity_type)

        try:
            entity_ids = None
            amount = 0

            if self.source == Source.wedatanation:
                amount, entity_ids = self.calculate_wedatanation_reward()
            
            if self.source == Source.litterbux:
                amount, entity_ids = self.calculate_litterbux_reward()

            elif self.source == Source.recyclium:
                amount = self.amount
            else:
                if start_date.date() >= datetime.today().date():
                    raise CannotClaimRewardException(f'Last reward payout date is today.')

                amount = self.calculate_amount_in_wei(start_date=start_date)

            if amount == 0:
                raise CannotClaimRewardException(ClaimRewardErrorMessages.ZERO_AMOUNT)

            if self.min_amount > amount:
                raise CannotClaimRewardException(ClaimRewardErrorMessages.AMOUNT_TOO_SMALL)

            sender_address = Account.from_key(config["rewards"]["account_private_key"]).address
            rewards_dao.update_claim_to_transferring(claim_id, amount, config["rewards"]["token_contract_address"],
                                                     sender_address, entity_ids=entity_ids)
            transaction_hash = self.transfer(amount)
            rewards_dao.update_claim_as_successful(claim_id, transaction_hash, entity_ids=entity_ids)
            logging.info("Reward transfer transaction for user [%s]: [%s]", self.public_address, transaction_hash)
            if self.source == Source.wedatanation:
                for entity_id in entity_ids:
                    parent_doc = image_metadata_dao.get_doc_by_id(entity_id)
                    parent_doc["reward_information"]["reward_status"] = EntityRewardStatus.paid
                    parent_doc["reward_information"]["claim_id"] = claim_id
                    image_metadata_dao.update_doc(doc_id=parent_doc["_id"], data=parent_doc)

                self.transfer_gas_if_needed()
            
            if self.source == Source.litterbux:
                self.update_litterbux_reward(amount)

            self.successful = True
            return transaction_hash

        except HTTPError as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except DBResultError as err:
            self.messages.append("Internal database error")
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except CannotClaimRewardException as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))

        except ContractLogicError as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except Exception as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

    def transfer(self, amount: int) -> str:
        # Constants
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        token_contract_address = Web3.toChecksumAddress(config["rewards"]["token_contract_address"])
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)
        contract = web3.eth.contract(address=token_contract_address, abi=ERC20_ABI)
        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(self.public_address), f"Not a valid address: {self.public_address}"

        txn = contract.functions.transfer(self.public_address, amount).buildTransaction(
            {'nonce': nonce, 'gas': 100000, 'chainId': chain_id})

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

    def transfer_gas_if_needed(self):
        # send gas to user only 1 time
        user_obj = user_dao.get_by_public_address(self.public_address)["result"][0]

        if user_obj.get("gas_transferred") is True:
            return

        logging.info("Transferring gas token to user [%s]", self.public_address)
        # now transfer some gas to user.
        amount = 0.01
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)

        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(self.public_address), f"Not a valid address: {self.public_address}"

        tx = {
            'nonce': nonce,
            'to': self.public_address,
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'chainId': chain_id
        }

        # sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=sender_account_private_key)
        tx_hash = signed_tx.hash.hex()

        # send transaction
        web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info("Gas transfer: Getting transaction receipt for tx [%s]", tx_hash)

        tx_receipt = web3.eth.wait_for_transaction_receipt(signed_tx.hash.hex())
        if tx_receipt is not None and tx_receipt['status'] != 1:
            raise CannotClaimRewardException(f"Transaction receipt status [{tx_receipt['status']}] when sending gas")
        # get transaction hash
        logging.info("Gas sent to user [%s]", self.public_address)

        user_obj["gas_transferred"] = True
        user_obj["gas_transfer_tx"] = tx_hash

        user_dao.save(user_obj["_id"], user_obj)

        return tx_hash

class ClaimRewardByQRCodeCommand(BaseCommand):

    def __init__(self, public_address: str, source: Source, entity_type: EntityType = None, amount: str = None):
        super(ClaimRewardByQRCodeCommand, self).__init__()
        self.public_address = public_address
        self.entity_type = entity_type
        self.source = source
        self.min_amount = 1
        self.amount = amount
        
    def execute(self):
        self.successful = False

        claim_id = rewards_dao.create_new_claim(self.public_address, datetime.now(), datetime.now(),
                                                self.source, self.entity_type)

        try:
            entity_ids = None
            amount = self.amount * (10 ** 18)

            sender_address = Account.from_key(config["rewards"]["account_private_key"]).address
            rewards_dao.update_claim_to_transferring(claim_id, amount, config["rewards"]["token_contract_address"],
                                                     sender_address, entity_ids=entity_ids)
            transaction_hash = self.transfer(amount)
            rewards_dao.update_claim_as_successful(claim_id, transaction_hash, entity_ids=entity_ids)
            logging.info("Reward transfer transaction for user [%s]: [%s]", self.public_address, transaction_hash)

            self.successful = True
            return transaction_hash

        except HTTPError as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except DBResultError as err:
            self.messages.append("Internal database error")
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except CannotClaimRewardException as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))

        except ContractLogicError as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

        except Exception as err:
            self.messages.append(str(err))
            rewards_dao.update_claim_to_failed(claim_id, str(err))
            logging.error(err, exc_info=True)

    def transfer(self, amount: int) -> str:
        # Constants
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        token_contract_address = Web3.toChecksumAddress(config["rewards"]["token_contract_address"])
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)
        contract = web3.eth.contract(address=token_contract_address, abi=ERC20_ABI)
        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(self.public_address), f"Not a valid address: {self.public_address}"

        txn = contract.functions.transfer(self.public_address, int(amount)).buildTransaction(
            {'nonce': nonce, 'gas': 100000, 'chainId': chain_id})

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

    def transfer_gas_if_needed(self):
        # send gas to user only 1 time
        user_obj = user_dao.get_by_public_address(self.public_address)["result"][0]

        if user_obj.get("gas_transferred") is True:
            return

        logging.info("Transferring gas token to user [%s]", self.public_address)
        # now transfer some gas to user.
        amount = 0.01
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)

        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(self.public_address), f"Not a valid address: {self.public_address}"

        tx = {
            'nonce': nonce,
            'to': self.public_address,
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'chainId': chain_id
        }

        # sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=sender_account_private_key)
        tx_hash = signed_tx.hash.hex()

        # send transaction
        web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info("Gas transfer: Getting transaction receipt for tx [%s]", tx_hash)

        tx_receipt = web3.eth.wait_for_transaction_receipt(signed_tx.hash.hex())
        if tx_receipt is not None and tx_receipt['status'] != 1:
            raise CannotClaimRewardException(f"Transaction receipt status [{tx_receipt['status']}] when sending gas")
        # get transaction hash
        logging.info("Gas sent to user [%s]", self.public_address)

        user_obj["gas_transferred"] = True
        user_obj["gas_transfer_tx"] = tx_hash

        user_dao.save(user_obj["_id"], user_obj)

        return tx_hash
