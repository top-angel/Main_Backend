from flask_api_key import APIKey
from config import config
from dao.base_dao import BaseDao
from datetime import datetime
from models.UserApiKey import UserApiKey
from utils.get_random_string import get_random_string


class UserApiKeyDao(BaseDao):
    def save_key(self, uuid: str, label: str, hashed_key: str, friendly_uuid: str):
        ak = UserApiKey(uuid, label, hashed_key, friendly_uuid)
        self.save(uuid, ak._dict())
        return ak._dict()
    
    def get_key(self, uuid: str):
        selector = {
            "selector": {"_id": {"$gt": None}, "uuid": uuid}
        }
        ret = self.query_data(selector)["result"]
        if len(ret) == 1:
            return UserApiKey(
                ret[0].get('uuid'), 
                ret[0].get('label'),
                ret[0].get('hashed_key'), 
                ret[0].get('friendly_uuid'),
            )
        
        return None

userapikey_dao = UserApiKeyDao()
userapikey_dao.set_config(
    config["couchdb"]["user"],
    config["couchdb"]["password"],
    config["couchdb"]["db_host"],
    config["couchdb"]["apikey_db"],
)
