from mongo_db import db


class Sensor(db.Document):
    sensor = db.StringField()

    def to_json(self):
        return {"id": str(self.id), "sensor": self.sensor}
