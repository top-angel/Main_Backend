from config import config
from commands.base_command import BaseCommand
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
import requests
from utils import crypto

class FileCoinDecryptDataCommand(BaseCommand):
    def __init__(self, nft_address, file_url):
        super().__init__()
        self.nft_address = nft_address
        self.file_url = file_url

    def execute(self):
        ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])

        ocean = Ocean(ocean_config)
    
        data_nft = ocean.get_nft_token(self.nft_address)

        symkey_asymenc2 = data_nft.get_data("symkey".encode())
        
        symkey2 = crypto.asym_decrypt(symkey_asymenc2.decode(), config["rewards"]["ocean_privkey"])

        data_symenc2  = requests.get(self.file_url).text

        data = crypto.sym_decrypt(data_symenc2, symkey2)

        return data

