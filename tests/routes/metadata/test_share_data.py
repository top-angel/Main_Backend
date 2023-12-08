import unittest
import json
import os
import requests

from models.metadata.annotations.annotation_type import AnnotationType
from models.metadata.metadata_models import Source
from tests.routes.metadata.test_metadata import TestMetadata
from utils.get_project_dir import get_project_root
from tests.test_base import TestBase

from config import config
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean


class TestShareData(TestBase):
    def __init__(self, *args, **kwargs):
        self.db_host = ""
        self.data_dir = os.path.join(get_project_root(), "data")
        self.dummy_data_path = os.path.join(get_project_root(), "tests", "data")
        super(TestShareData, self).__init__(*args, **kwargs)

    def create_data_share(self):
        acct = self.default_accounts[0]

        token = TestMetadata.get_token_for_account(acct, source=Source.brainstem)
        headers = {"Authorization": "Bearer {0}".format(token)}

        api_url = self.url + "/api/v1/metadata/create-data-share"

        response = requests.request(
            "POST", api_url, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        data_share_id = data["data_share_id"]
        self.assertTrue(data_share_id is not None)


    def share_data(self):
        acct = self.default_accounts[0]

        token = TestMetadata.get_token_for_account(acct, source=Source.brainstem)
        headers = {"Authorization": "Bearer {0}".format(token)}

        api_url = self.url + "/api/v1/metadata/create-data-share"

        response = requests.request(
            "POST", api_url, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        data_share_id = data["data_share_id"]
        self.assertTrue(data_share_id is not None)

        consumer = self.default_accounts[1]
        api_url = self.url + "/api/v1/metadata/share-data?data_share_id={}&to_address={}".format(data_share_id, consumer.address)

        response = requests.request(
            "POST", api_url, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        mint_tx = data["mint_tx"]
        self.assertTrue(mint_tx is not None)


    def download_share_data(self):
        ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])
        ocean = Ocean(ocean_config)

        owner = self.default_accounts[0]
        consumer = self.default_accounts[1]

        consumer_wallet = Wallet(
            ocean.web3,
            consumer.key,
            ocean_config["BLOCK_CONFIRMATIONS"],
            ocean_config["TRANSACTION_TIMEOUT"],
        )

        # Owner creates data share
        token = TestMetadata.get_token_for_account(owner, source=Source.brainstem)
        headers = {"Authorization": "Bearer {0}".format(token)}

        api_url = self.url + "/api/v1/metadata/create-data-share"

        response = requests.request(
            "POST", api_url, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data_share = json.loads(response.text)['result']
        self.assertTrue(data_share["data_share_id"] is not None)

        # Owner shares the data to the consumer
        api_url = self.url + "/api/v1/metadata/share-data?data_share_id={}&to_address={}".format(data_share["data_share_id"], consumer.address)

        response = requests.request(
            "POST", api_url, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        mint_tx = data["mint_tx"]
        self.assertTrue(mint_tx is not None)

        # Consumer downloads the data

        # To download data, consumer should start order with the data token
        # Get the necessary params for startOrder
        consumer_token = TestMetadata.get_token_for_account(consumer, source=Source.brainstem)
        api_url = self.url + "/api/v1/compute/data/data-share-order-params/{}?data_share_id={}".format(consumer_token, data_share['data_share_id'])

        response = requests.request(
            "GET", api_url
        )

        self.assertEqual(response.status_code, 200)
        params = json.loads(response.text)

        provider_fees = params['provider_fees']
        data_token = ocean.get_datatoken(data_share["data_token_address"])
        order_tx_hash = data_token.start_order(
            consumer=consumer.address,
            service_index=params["service_index"],
            provider_fee_address=provider_fees["providerFeeAddress"],
            provider_fee_token=provider_fees["providerFeeToken"],
            provider_fee_amount=provider_fees["providerFeeAmount"],
            v=provider_fees["v"],
            r=provider_fees["r"],
            s=provider_fees["s"],
            valid_until=provider_fees["validUntil"],
            provider_data=provider_fees["providerData"],
            consume_market_order_fee_address=params["consume_market_order_fee_address"],
            consume_market_order_fee_token=params["consume_market_order_fee_token"],
            consume_market_order_fee_amount=params["consume_market_order_fee_amount"],
            from_wallet=consumer_wallet,
        )

        # Download the data share

        api_url = self.url + "/api/v1/compute/data/download-share-data-zip/{}?data_share_id={}&order_tx_hash={}".format(consumer_token, order_tx_hash)

        response = requests.request(
            "GET", api_url
        )

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
