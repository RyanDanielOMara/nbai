from database.tables.fields import Fields as f
from web_api.nodes.basenode import BaseNode



class RosterNode(BaseNode):
    def __init__(self, nba_data, team_id):
        setattr(self, f.team_id, team_id)
        setattr(self, f.roster, [int(p['PLAYER_ID']) for p in nba_data])
        return

