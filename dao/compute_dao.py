import datetime

from dao.base_dao import BaseDao
from config import config
from utils.get_random_string import get_random_string


class ComputeDao(BaseDao):
    def __init__(self):
        super().__init__()

    def create_compute_input(self, public_address: str, entity_list_id: str, parameters: dict) -> str:
        doc_id = get_random_string(15)
        document = dict()
        document['public_address'] = public_address
        document['entity_list_id'] = entity_list_id
        document['parameters'] = parameters
        document['created_at'] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
        return self.save(doc_id, document)['id']

    def get_compute_info(self, doc_id: str) -> dict:
        return self.get_doc_by_id(doc_id)


compute_dao = ComputeDao()
compute_dao.set_config(
    config["couchdb"]["user"],
    config["couchdb"]["password"],
    config["couchdb"]["db_host"],
    config["couchdb"]["compute_db"],
)
