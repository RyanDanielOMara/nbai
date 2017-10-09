from database.connection import connection
from database.tables._base import DatabaseRecord
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



TABLE_NAME = 'players'

@connection.register
class PlayerRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.player_id   : s.player_id,
        f.player_name : s.player_name,
        f.team_id     : s.team_id,
        f.games_dict  : s.games_dict,
        f.weight      : s.weight,
        f.height      : s.height,
        f.dob         : s.dob,
        f.country     : s.country,
        f.first_year  : s.first_year,
        f.last_year   : s.last_year,
        f.exp         : s.exp,
        f.position    : s.position,
        f.jersey      : s.jersey,
        f.has_bio     : s.has_bio,
    }

    indexes = [
        {
            'fields' : [f.player_id],
            'unique' : True
        }
    ]

    required_fields = [
        f.player_id,
    ]

    default_values = {
        f.has_bio : False,
    }

