from dao.users_dao import user_dao
from dao.metadata_dao import image_metadata_dao
from models.metadata.metadata_models import FileLocation, EntitySubType
from models.metadata.annotations.annotation_type import AnnotationType
from commands.base_command import BaseCommand
from config import config
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.utils.utilities import create_checksum
from datetime import datetime

class CreateDataShareCommand(BaseCommand):

    def __init__(self, public_address: str):
        super().__init__(public_address=public_address)
        self.user_dao = user_dao
        self.image_metadata_dao = image_metadata_dao

    def execute(self):
        self.successful = True
        
        # location = FileLocation.server
        source = 'brainstem'
        # design_doc = "query-metadata"
        # view_name = "downloadable-user-docs-for-zip"

        # start_key = f'["{source}","{self.public_address}","{location}"]'
        # end_key = (
        #     f'["{source}","{self.public_address}","{location}",{{}}]'
        # )

        # result = image_metadata_dao.query_view_by_key_range(design_doc=design_doc,
        #                                                     view_name=view_name,
        #                                                     start_key=start_key,
        #                                                     end_key=end_key,
        #                                                     skip=0,
        #                                                     group_level=0,
        #                                                     limit=1)

        # if not len(result['rows']) > 0:
        #     self.messages.append("You didn't upload any data yet.")
        #     self.successful = False
        #     return

        ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])

        ocean = Ocean(ocean_config)

        account_private_key = config["rewards"]["account_private_key"]

        web3_wallet = Wallet(
            ocean.web3,
            account_private_key,
            ocean_config["BLOCK_CONFIRMATIONS"],
            ocean_config["TRANSACTION_TIMEOUT"],
        )

        is_new = False
        data_nft_address = user_dao.get_data_nft_address(self.public_address)
        if data_nft_address:
            data_nft = ocean.get_nft_token(data_nft_address)
        else:
            data_nft = ocean.create_data_nft(
                name="Brainstem NFT",
                symbol="BSNFT",
                from_wallet=web3_wallet,
                additional_datatoken_deployer=web3_wallet.address,
                additional_metadata_updater=web3_wallet.address,
                # Optional parameters
                token_uri="https://www.dataunion.app/wp-content/uploads/elementor/thumbs/logo2-pq2gnen6pz25kw859sdyuyyh23xml7r7wpzn9jqtq8.png",
                template_index=1,
                transferable=True,
                owner=self.public_address,
            )
            # data_nft.add_manager(manager_address=self.public_address, from_wallet=web3_wallet)
            user_dao.set_data_nft_address(self.public_address, data_nft.address)
            is_new = True

        fee_manager = ZERO_ADDRESS
        publish_market_order_fee_address = ZERO_ADDRESS
        publish_market_order_fee_token = ZERO_ADDRESS
        minter = web3_wallet.address
        publish_market_order_fee_amount = 0

        data_token = data_nft.create_datatoken(
            name="Brainstem Datatoken",
            symbol="BSDT",
            datatoken_cap=ocean.to_wei(1000),
            from_wallet=web3_wallet,
            # Ootional parameters below
            template_index=2,
            fee_manager=fee_manager,
            publish_market_order_fee_token=publish_market_order_fee_token,
            publish_market_order_fee_amount=publish_market_order_fee_amount,
            minter=minter,
            publish_market_order_fee_address=publish_market_order_fee_address,
        )

        data_token.create_dispenser(
            dispenser_address=ocean.dispenser.address,
            max_balance=ocean.to_wei(1000),
            max_tokens=ocean.to_wei(1000),
            with_mint=True,
            allowed_swapper=ZERO_ADDRESS,
            from_wallet=web3_wallet,
        )

        if is_new:
            date_created = datetime.now().isoformat()
            metadata = {
                "created": date_created,
                "updated": date_created,
                "description": "Brainsteam dataset - DataUnion",
                "name": "Brainstem Dataset",
                "type": "dataset",
                "author": "Dataunion",
                "license": "CC0: PublicDomain",
            }

            # TODO: Change this url to the data or something related to brainstem
            url = "https://filesamples.com/samples/code/json/sample1.json"
            files = [UrlFile(url)]

            asset = ocean.assets.create(
                metadata=metadata,
                publisher_wallet=web3_wallet,
                files=files,
                data_nft_address=data_nft.address,
                deployed_datatokens=[data_token]
            )
        else:
            did = (
                f"did:op:{create_checksum(data_nft.address + str(ocean.web3.eth.chain_id))}"
            )
            asset = ocean.assets.resolve(did)

        doc_id = image_metadata_dao.generate_new_doc_id()

        child_doc_id = image_metadata_dao.generate_new_doc_id()
        child_doc_id = image_metadata_dao.add_new_child_entity(child_doc_id, self.public_address, doc_id, {}, EntitySubType.data_share, source)

        document = {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "uploaded_by": self.public_address,
            "data_nft_address": data_nft.address,
            "data_token_address": data_token.address,
            "did": asset.did,
            "type": "json",
            "json_entity_type": EntitySubType.data_share,
            "annotations_required": [AnnotationType.data_share_report],
            "available_for_annotation": True,
            "child_docs": [child_doc_id],
            "user_submissions": {
                AnnotationType.data_share_report: []
            },
            "shares": {}
        }

        image_metadata_dao.save(doc_id, document)

        return {
            "data_share_id": doc_id,
            "did": asset.did,
            "data_nft_address": data_nft.address,
            "data_token_address": data_token.address,
        }


