import logging
import os

from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from web3 import Web3
from dao.rewards_dao import rewards_dao
from config import config
import sys
from models.metadata.metadata_models import EntityType

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

token_address = config['rewards']['public_address']
network_url = config['rewards']['network_url']

ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])
ocean = Ocean(ocean_config)
datatoken_contract_address = Web3.toChecksumAddress(config["rewards"]["datatoken_contract_address"])
datatoken = ocean.get_data_token(datatoken_contract_address)

transfers = datatoken.get_event_logs(event_name="Transfer", filter_args={"from": token_address})
# w3 = Web3(Web3.HTTPProvider(network_url))

for transfer in transfers:
    # tx = w3.eth.get_transaction(transfer.transactionHash)
    tx_hash = transfer.transactionHash.hex()
    if rewards_dao.is_transaction_already_saved(tx_hash):
        logging.info(f"Transaction already saved. Skipping [{tx_hash}]")
        continue

    rewards_dao.save_record_from_blockchain(sender=transfer.args['from'], receiver=transfer.args['to'],
                                            network_name='rinkeby',
                                            amount=transfer.args['value'], entity_type=EntityType.image,
                                            transaction_hash=tx_hash,
                                            block_number=transfer.blockNumber)
