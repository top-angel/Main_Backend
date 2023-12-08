from config import config
from commands.base_command import BaseCommand
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from web3 import Web3
from utils import crypto
import requests

class FileCoinEncryptDataCommand(BaseCommand):
    def __init__(self, public_address, label, value):
        super().__init__(public_address=public_address)
        self.label = label
        self.value = value

    def execute(self):
        ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])

        ocean = Ocean(ocean_config)

        account_private_key = config["rewards"]["account_private_key"]

        web3_wallet = Wallet(
            ocean.web3,
            account_private_key,
            ocean_config["BLOCK_CONFIRMATIONS"],
            ocean_config["TRANSACTION_TIMEOUT"],
        )

        data_nft = ocean.create_data_nft(
            name="DataUnion NFT",
            symbol="DUNFT",
            from_wallet=web3_wallet,
            additional_datatoken_deployer=web3_wallet.address,
            additional_metadata_updater=web3_wallet.address,
            # Optional parameters
            token_uri="https://www.dataunion.app/wp-content/uploads/elementor/thumbs/logo2-pq2gnen6pz25kw859sdyuyyh23xml7r7wpzn9jqtq8.png",
            template_index=1,
            transferable=True,
            owner=web3_wallet.address,
        )

        symkey = crypto.calc_symkey(data_nft.address + self.label + web3_wallet.private_key)

        # Symmetrically encrypt AI model
        model_value_symenc = crypto.sym_encrypt(self.value.decode('cp437'), symkey)

        files = {
            'file': model_value_symenc
        }

        ### ADD FILE TO IPFS AND SAVE THE HASH ###
        response = requests.post(config["ipfs"]["endpoint"] + '/api/v0/add', files=files, auth=(config["ipfs"]["api_key"], config["ipfs"]["api_secret"]))
        hash = response.text.split(",")[1].split(":")[1].replace('"','')

        symkey_asymenc = crypto.asym_encrypt(symkey, config["rewards"]["ocean_pubkey"])

        # Save symkey to chain
        data_nft.set_new_data(
            key="symkey".encode(),
            value=symkey_asymenc.encode(),
            from_wallet=web3_wallet
        )

        return {
            "nft_address": data_nft.address,
            "symkey": symkey,
            "label": self.label,
            "url": "https://ipfs.io/ipfs/{}".format(hash)
        }
