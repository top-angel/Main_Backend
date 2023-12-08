import os
from commands.base_command import BaseCommand
from dao.guild_dao import guild_dao
from dao.users_dao import user_dao
from werkzeug.utils import secure_filename
from config import config

class GetGuildByIdCommand(BaseCommand):
    def __init__(self, guild_id: str):
        super(GetGuildByIdCommand, self).__init__()
        self.guild_id = guild_id
    
    def execute(self):
        guilds = guild_dao.fetch_guild_by_id(self.guild_id)
        self.successful = True
        return guilds
    

class FetchGuildListCommand(BaseCommand):
    def __init__(self):
        super(FetchGuildListCommand, self).__init__()
    
    def execute(self):
        guilds = guild_dao.fetch_guild_list()
        self.successful = True
        return guilds
        
class JoinGuildCommand(BaseCommand):
    def __init__(self, public_address: str, guild_id: str):
        super(JoinGuildCommand, self).__init__()
        self.public_address = public_address
        self.guild_id = guild_id
    
    def execute(self):
        user_info = user_dao.get_by_public_address(self.public_address)["result"]
        if len(user_info) != 1:
            self.successful = False
            self.messages.append(f"User {self.public_address} not exists.")
            return

        guild_info = guild_dao.fetch_guild_by_id(self.guild_id)
        if guild_info == None:
            self.successful = False
            self.messages.append(f"Guild {self.guild_id} not exists")
            return
        
        guild_dao.add_user_to_guild(user_info[0]["public_address"], self.guild_id)
        user_dao.set_guild(user_info[0]["public_address"], self.guild_id)
        
        user_reward_amount = user_info[0].get("rewards", 0)
        if user_reward_amount > 0:
            guild_dao.add_guild_rewards(self.guild_id, user_reward_amount)
        
        self.successful = True
        return

class LeaveGuildCommand(BaseCommand):
    def __init__(self, public_address: str, guild_id: str):
        super(LeaveGuildCommand, self).__init__()
        self.public_address = public_address
        self.guild_id = guild_id
        
    def execute(self):
        user_info = user_dao.get_by_public_address(self.public_address)["result"]
        if len(user_info) != 1:
            self.successful = False
            self.messages.append(f"User {self.public_address} not exists.")
            return
        if self.guild_id == "":
            self.successful = False
            self.messages.append(f"User {self.public_address} is not in guild.")
            return

        guild_info = guild_dao.fetch_guild_by_id(self.guild_id)
        if guild_info == None:
            self.successful = False
            self.messages.append(f"Guild {self.guild_id} not exists")
            return
        
        guild_dao.remove_user_from_guild(user_info[0]["public_address"], self.guild_id)
        user_dao.set_guild(user_info[0]["public_address"], "")
        
        user_reward_amount = 0
        if user_info[0]["rewards"] != None and user_info[0]["rewards"] > 0:
            user_reward_amount = user_info[0]["rewards"]
            guild_dao.add_guild_rewards(self.guild_id, user_reward_amount * -1)
        
        self.successful = True
        return


class CreateGuildCommand(BaseCommand):
    def __init__(self, public_address: str, name: str, description: str,
                 invited_users: list, profile_image):
        super(CreateGuildCommand, self).__init__()
        self.public_address = public_address
        self.name = name
        self.description = description
        self.invited_users = invited_users
        self.profile_image = profile_image
        self.guild_dao = guild_dao

    def execute(self):
        if not self.validate_profile_image():
            self.successful = False
            return
        
        # check same guild exists
        existing_guild = guild_dao.get_guild_by_name(self.name)
        if existing_guild != None:
            self.successful = False
            self.messages.append("Guild already exists")
            return

        dir_path = os.path.join(
        config["application"]["upload_folder"], self.public_address, "temp"
        )
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        profile_image_filename = secure_filename(self.profile_image.filename)
        profile_image_file_path = os.path.join(dir_path, 'guild-' + profile_image_filename)
        self.profile_image.save(profile_image_file_path)

        description_limit = 2000
        if self.description and len(self.description) > description_limit:
            self.successful = False
            self.messages.append(f"Description too long. Limit is {description_limit} characters.")
            return

        name_limit = 200
        if self.description and len(self.name) > name_limit:
            self.successful = False
            self.messages.append(f"Name too long. Limit is {name_limit} characters.")
            return
        
        # add creator in member list
        members = [self.public_address]
        
        # retrieve creator info
        creator_info = user_dao.get_by_public_address(self.public_address)["result"]
        if len(creator_info) != 1:
            self.successful = False
            self.messages.append(f"Guild creator {self.public_address} is invalid.")
            return
        guild_balance = creator_info[0].get("rewards", 0)
        
        guild, guild_id = guild_dao.create_guild(
            self.public_address,
            self.name,
            self.description,
            members,
            self.invited_users,
            profile_image_filename,
            profile_image_file_path,
            rewards=guild_balance
        )
        
        # set guild info
        user_dao.set_guild(self.public_address, guild_id)

        self.successful = True
        return guild
    
    def validate_profile_image(self):
        if not self.profile_image or not self.profile_image.filename:
            self.messages.append("Profile image not found.")
            return False

        return True
