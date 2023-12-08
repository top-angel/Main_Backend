
import os
from commands.base_command import BaseCommand
from flask_api_key.api_key import APIKey
from flask_api_key.utils import get_api_key_manager
from config import config

class ApiKeyCommand(BaseCommand):
    def __init__(self, label: str):
        super(ApiKeyCommand, self).__init__()
        self.label = label
    
    def execute(self):
      mgr = get_api_key_manager()
      ak = mgr.create(self.label)
      print(ak)
      
      self.successful = True
      return ak


if __name__ == "__main__":
  c = ApiKeyCommand(config['application'].get('api_key_label'))
  c.execute()
  assert c.successful