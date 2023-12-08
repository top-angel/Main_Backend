from enum import Enum


class DatabaseName(str, Enum):
    metadata = "metadata"
    bounty = "bounty"
    entity_list = "entity_list"
    static_data = "static_data"
    users = "users"
    other = "other"
    missions = "missions"
    guild_db = "guild_db"
