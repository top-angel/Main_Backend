from collections import defaultdict

from commands.base_command import BaseCommand
from dao.users_dao import user_dao
from dao.metadata_dao import image_metadata_dao
from dao.others_dao import others_db
from datetime import datetime

class RankUserCommand(BaseCommand):
    def __init__(self):
        super(RankUserCommand, self).__init__()
    
    def execute(self):
        guilds = user_dao.get_user_rank_by_rewards()
        self.successful = True
        return guilds

if __name__ == "__main__":
    c = RankUserCommand()
    c.execute()
    assert c.successful
