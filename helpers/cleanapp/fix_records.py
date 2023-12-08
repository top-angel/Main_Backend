import random
from config import config
from dao.users_dao import user_dao
from commands.dataunions.litterbux.add_rewards_command import AddRewardsCommand
from models.metadata.metadata_models import EntityRewardStatus

from models.User import TeamType

if __name__ == "__main__":
    all_users = user_dao.get_all()["result"]
    all_users = [all_users[0]]
    addresses = [user['public_address'] for user in all_users]
    
    for addr in set(addresses):
        users = user_dao.get_by_public_address(addr)['result']
        print(addr)
        print(len(users))
        if len(users) > 0:
            first_user = users[0]
            print(first_user['_id'])
            updated = False
            if (len(users)> 1):
                for user in users:
                    if user['_id'] == first_user['_id']:
                        continue
                    if first_user.get('team') == None and user.get('team'):
                        first_user['team'] = user.get('team')
                        updated = True
                    if first_user.get('tutorial_reward_status') == None and user.get('tutorial_reward_status'):
                        first_user['tutorial_reward_status'] = user.get('tutorial_reward_status')
                        updated = True
                    if first_user.get('data_sharing_option') == None and user.get('data_sharing_option'):
                        first_user['data_sharing_option'] = user.get('data_sharing_option')
                        updated = True
                    if user.get('rewards'):
                        if first_user.get('rewards'):
                            first_user['rewards'] = first_user['rewards'] + user.get('rewards') -10
                        else:
                            first_user['rewards'] = user.get('rewards')
                        updated = True
                    if first_user.get('guild_id') == None and user.get('guild_id'):
                        first_user['guild_id'] = user.get('guild_id')
                        updated = True
                    user_dao.delete_doc(user['_id'])
            if not first_user.get('team'):
                team_choice = random.choice([0, 1])
                team_name = TeamType.blue if team_choice == 0 else TeamType.green
                first_user['team'] = team_name
                updated = True
            if updated:
                user_dao.update_doc(first_user['_id'], first_user)
            point = config["application"].getint("reward_start_tutorial", 10)
            if not first_user.get('tutorial_reward_status'):
                user_dao.set_tutorial_reward_claimed(addr, EntityRewardStatus.unpaid)
                reward_c = AddRewardsCommand(addr, point)
                reward_c.execute()
