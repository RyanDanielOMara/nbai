from _base import DatabaseRecord
from connection import connection
from fields import Fields as f
from fields import Structure as s

TABLE_NAME = 'teams'

@connection.register
class TeamRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.team_id    : s.team_id,
        f.team_name  : s.team_name,
        f.team_abbr  : s.team_abbr,
        f.division   : s.division,
        f.conference : s.conference,
        f.color      : s.color,
        f.colors     : s.colors,
        f.roster     : s.roster,
        f.games_dict : s.games_dict,
    }

    indexes = [
        {
            'fields' : [f.team_id],
            'unique' : True
        }
    ]

    required_fields = [
        f.team_id,
        f.team_name,
        f.team_abbr,
        f.division,
        f.conference,
        f.color,
        f.colors,
    ]

    default_values = {
    }

