class UserApiKey:
  def __init__(
    self,
    uuid,
    label,
    hashed_key,
    friendly_uuid,
  ):
    self.uuid = uuid
    self.label = label
    self.hashed_key = hashed_key
    self.friendly_uuid = friendly_uuid
  
  def _dict(self):
    return {
      'uuid': self.uuid,
      'label': self.label,
      'hashed_key': self.hashed_key,
      'friendly_uuid': self.friendly_uuid,
    }
