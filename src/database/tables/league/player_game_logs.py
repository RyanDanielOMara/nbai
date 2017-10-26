from database.connection import connection
from database.tables.league._game_logs import GameLogRecord
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



TABLE_NAME = 'player_game_logs'

@connection.register
class PlayerGameLogRecord(GameLogRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.player_game_id : s.player_game_id,
        f.player_id      : s.player_id,
        f.player_name    : s.player_name,
    }

    indexes = [
        {
            'fields' : [f.player_game_id],
            'unique' : True
        }
    ]

    required_fields = [
        f.player_game_id,
        f.player_id,
        f.player_name,
    ]

    default_values = {
    }

