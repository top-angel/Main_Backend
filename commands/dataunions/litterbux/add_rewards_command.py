from collections import defaultdict

from commands.base_command import BaseCommand
from dao.users_dao import user_dao
from dao.metadata_dao import image_metadata_dao
from dao.others_dao import others_db
from dao.guild_dao import guild_dao
from datetime import datetime
from models.User import TeamType
from commands.dataunions.litterbux.team_management import AddTeamPointCommand

class AddRewardsCommand(BaseCommand):
  def __init__(self, public_address: str, point: int):
    super(AddRewardsCommand, self).__init__()
    self.public_address = public_address
    self.point = point

  def execute(self):
    user = user_dao.get_by_public_address(self.public_address)["result"]
    if len(user) != 1:
      self.successful = False
      self.messages.append(f"User {self.public_address} not exists.")
      return
    
    # add user reward point
    user_dao.add_reward_balance(self.public_address, self.point)
    
    guild_id = user[0].get("guild_id")
    if guild_id != None:
      guild_dao.add_guild_rewards(guild_id, self.point)
 
    # team add reward
    team_c = AddTeamPointCommand(self.public_address, self.point)
    team_c.execute()
    
    self.successful = True
    return

if __name__ == "__main__":
  c = AddRewardsCommand()
  c.execute()
  assert c.successful
