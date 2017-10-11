from database.tables.fields import Fields as f
from web_api.nodes.basenode import BaseNode



class ScheduleNode(BaseNode):

    def __init__(self, nba_data):
        self.attrs = {
            f.game_date      : None,
            f.game_id        : None,
            f.team_id        : None,
            f.team_game_id   : None,
            f.is_home        : None,
            f.game_log_saved : None,
        }

        self.parsers = {
        }

        self.init_attrs(nba_data)
        return

