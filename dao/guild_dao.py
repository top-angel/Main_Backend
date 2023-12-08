from datetime import datetime
from config import config
from dao.base_dao import BaseDao

class GuildDao(BaseDao):
    def __init__(self):
        super(GuildDao, self).__init__()
        self.id_prefix = "guild"

    def create_guild(self,
                    public_address: str,
                    name: str,
                    description: str,
                    members: list,
                    invited_members: list,
                    profile_image_filename: str,
                    profile_image_file_path: str,
                    rewards=0
        ):
        
        doc_id = guild_dao.generate_new_doc_id()
        created_time = datetime.now().replace(microsecond=0).isoformat()

        document = {
            'updated_at': created_time,
            'created_at': created_time,
            'created_by': public_address,
            'name': name,
            'description': description,
            'members': members,
            'invited_members': invited_members,
            'profile_image_filename': profile_image_filename,
            'profile_image_file_path': profile_image_file_path,
            'rewards': rewards
        }
        self.save(doc_id, document)
        return document, doc_id
    
    def get_guild_by_name(self, guild_name: str):
        selector = {"selector": {"name": guild_name}}
        result = self.query_data(selector)["result"]
        if len(result) == 0:
            return None
        return result[0]
    
    def fetch_guild_by_id(self, guild_id: str):
        selector = {"selector": {"_id": guild_id}}
        result = self.query_data(selector)["result"]
        if len(result) != 1:
            return None
        return result[0]
    
    def remove_user_from_guild(self, public_address: str, guild_id: str):
        documents = self.fetch_guild_by_id(guild_id)
        if documents == None:
            return False

        if public_address in documents["members"]:
            documents["members"].remove(public_address)
        
        # deduct user balance from guild balance
        self.update_doc(documents["_id"], documents)
        return documents
    
    def add_user_to_guild(self, public_address: str, guild_id: str):
        documents = self.fetch_guild_by_id(guild_id)
        if documents == None:
            return None
        
        if "members" not in documents:
            documents["members"] = []
        
        if public_address not in documents["members"]:
            documents["members"].append(public_address)
        # add user balance from guild balance
        self.update_doc(documents["_id"], documents)
        return documents
        
    
    def fetch_guild_list(self):
        selector = {
            "sort": [{"rewards": "desc"}],
            "limit": 100000,
            "selector": {"_id": {"$gt": None}}}

        result = self.query_data(selector)["result"]
        return result
    
    def add_guild_rewards(self, guild_id: str, amount: int):
        documents = self.fetch_guild_by_id(guild_id)
        if documents == None:
            return None

        if "rewards" not in documents:
            documents["rewards"] = 0
            
        documents["rewards"] += amount
        if documents["rewards"] < 0:
            documents["rewards"] = 0
        self.update_doc(documents["_id"], documents)
        return documents


guild_dao = GuildDao()
guild_dao.set_config(
    config["couchdb"]["user"],
    config["couchdb"]["password"],
    config["couchdb"]["db_host"],
    config["couchdb"]["guild_db"],
)
