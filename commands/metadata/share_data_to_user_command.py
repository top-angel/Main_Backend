from dao.metadata_dao import image_metadata_dao
from commands.base_command import BaseCommand
from config import config
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from web3 import Web3

class ShareDataToUserCommand(BaseCommand):

    def __init__(self, to_address: str, data_share_id: str):
        super().__init__()
        self.to_address = Web3.toChecksumAddress(to_address)
        self.data_share_id = data_share_id
        self.image_metadata_dao = image_metadata_dao

    def execute(self):
        self.successful = True
        ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])

        ocean = Ocean(ocean_config)

        account_private_key = config["rewards"]["account_private_key"]

        web3_wallet = Wallet(
            ocean.web3,
            account_private_key,
            ocean_config["BLOCK_CONFIRMATIONS"],
            ocean_config["TRANSACTION_TIMEOUT"],
        )

        data_share = image_metadata_dao.get_doc_by_id(self.data_share_id)

        if not data_share:
            self.messages.append("Please create a Data Share first.")
            self.successful = False
            return

        data_token = ocean.get_datatoken(data_share['data_token_address'])
        tx = data_token.mint(
            account_address=self.to_address,
            value=ocean.to_wei("1"),
            from_wallet=web3_wallet,
        )

        data_share['shares'][self.to_address] = {
            "mint_tx_hash": tx,
            "order_tx_hash": ""
        }
        image_metadata_dao.save(data_share['_id'], data_share)

        return {
            "data_share_id": data_share['_id'],
            "mint_tx": tx
        }
