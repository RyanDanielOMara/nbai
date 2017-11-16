from _base import DatabaseRecord
from connection import connection
from fields import Fields as f
from fields import Structure as s



TABLE_NAME = 'player_predictions'

@connection.register
class PlayerPredictionRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.player_id   : s.player_id,
        f.game_id     : s.game_id,
        f.team_abbr   : s.team_abbr,
        f.prediction  : s.prediction,

    }

    indexes = [
        {
            'fields' : [f.player_id],
            'unique' : True
        }
    ]

    required_fields = [
        f.player_id,
        f.game_id,
        f.team_abbr,
        f.prediction  
    ]

    default_values = {
        
    }

