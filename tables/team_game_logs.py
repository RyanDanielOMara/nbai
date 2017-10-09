from _game_logs import GameLogRecord
from connection import connection
from fields import Fields as f
from fields import Structure as s



TABLE_NAME = 'team_game_log'

@connection.register
class TeamGameLogRecord(GameLogRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.team_game_id : s.team_game_id,
        f.roster       : s.roster,
    }

    indexes = [
        {
            'fields' : [f.team_game_id],
            'unique' : True
        }
    ]

    required_fields = [
        f.team_game_id,
        f.roster,
    ]

    default_values = {
    }

