import os
from commands.base_command import BaseCommand
from werkzeug.utils import secure_filename
from config import config
from dao.others_dao import others_db
from datetime import datetime
from models.User import TeamType
from dao.users_dao import user_dao

class GetTeamStatusCommand(BaseCommand):
  def __init__(self, public_address: str):
      super(GetTeamStatusCommand, self).__init__()
      self.doc_id = "litterbux-team"
      self.public_address = public_address
  
  def execute(self):
      exists, doc = others_db.get_if_exists(self.doc_id)
      if not exists:
        doc = {
          "created_at": datetime.utcnow().isoformat(),
          "data": [
            {
              "name": TeamType.blue,
              "point": 0
            },
            {
              "name": TeamType.green,
              "point": 0
            },
          ]
        }
        others_db.save(self.doc_id, doc)
      user = user_dao.get_by_public_address(self.public_address)["result"]
      if len(user) == 1:
        doc["user_data"] = {
          "team": user[0].get("team", TeamType.blue)
        }
      self.successful = True
      return doc

class AddTeamPointCommand(BaseCommand):
  def __init__(self, public_address: str, point: int):
    super(AddTeamPointCommand, self).__init__()
    self.doc_id = "litterbux-team"
    self.public_address = public_address
    self.point = point
  
  def execute(self):
    team_name = user_dao.get_team(self.public_address)
    exists, doc = others_db.get_if_exists(self.doc_id)
    if not exists:
      doc = {
        "created_at": datetime.utcnow().isoformat(),
        "data": [
          {
            "name": TeamType.blue,
            "point": 0
          },
          {
            "name": TeamType.green,
            "point": 0
          },
        ]
      }
      others_db.save(self.doc_id, doc)
      
    for k in range(len(doc["data"])):
      if doc["data"][k]["name"] == team_name:
        doc["data"][k]["point"] += self.point

    others_db.update_doc(self.doc_id, doc);    
    self.successful = True
    return doc        
