from datetime import datetime

from config import config
from dao.base_dao import BaseDao


class BatchDao(BaseDao):
    def __init__(self):
        super(BatchDao, self).__init__()
        self.id_prefix = "batch"

    def create_batch(self,
                    public_address: str,
                    product_id: str,
                    batch_name: str,
                    amount_of_items: int,
                    bounty_id: str,) -> str:
        doc_id = batch_dao.generate_new_doc_id()
        created_time = datetime.now().replace(microsecond=0).isoformat()

        document = {
            'updated_at': created_time,
            'created_at': created_time,
            'public_address': public_address,
            'product_id': product_id,
            'batch_name': batch_name,
            'amount_of_items': amount_of_items,
            'bounty_id': bounty_id,
        }

        self.save(doc_id, document)
        return doc_id

    def get_all_batches_not_signed_by_product_id(self, product_id: str):
        selector = {
            "selector": {
                "_id": {"$gt": None},
                "product_id": product_id,
                "bounty_id": None
            }
        }
        result = self.query_data(selector)["result"]
        return result

    def get_all_batches_by_product_id(self, product_id: str):
        selector = {
            "selector": {
                "_id": {"$gt": None},
                "product_id": product_id,
            }
        }
        result = self.query_data(selector)["result"]
        return result
    
    def set_bounty_id(self, batch_ids:list, bounty_id: str):
        for batch_id in batch_ids:         
            doc = self.get_doc_by_id(batch_id)
            doc["bounty_id"] = bounty_id
            self.update_doc(batch_id, doc)

        return True

batch_dao = BatchDao()
batch_dao.set_config(
    config["couchdb"]["user"],
    config["couchdb"]["password"],
    config["couchdb"]["db_host"],
    config["couchdb"]["batch_db"],
)
