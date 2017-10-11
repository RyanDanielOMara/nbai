from database.tables.fields import Fields as f
from web_api.nodes.basenode import BaseNode
from web_api.parsers import cast_int, is_home, is_win, get_player_game_id, get_team_game_id, get_game_date



class BaseGameNode(BaseNode):
    def __init__(self, nba_data):
        self.attrs = {
            f.game_id      : 'GAME_ID',
            f.team_id      : 'TEAM_ID',
            f.team_name    : 'TEAM_NAME',
            f.team_abbr    : 'TEAM_ABBREVIATION',
            f.game_date    : 'GAME_DATE',
            f.pts          : 'PTS',
            f.reb          : 'REB',
            f.oreb         : 'OREB',
            f.dreb         : 'DREB',
            f.ast          : 'AST',
            f.blk          : 'BLK',
            f.stl          : 'STL',
            f.plus_minus   : 'PLUS_MINUS',
            f.fouls        : 'PF',
            f.tov          : 'TOV',
            f.minutes      : 'MIN',
            f.fgm          : 'FGM',
            f.fga          : 'FGA',
            f.fg3m         : 'FG3M',
            f.fg3a         : 'FG3A',
            f.ftm          : 'FTM',
            f.fta          : 'FTA',
            f.won          : 'WL',
            f.is_home      : None,
            f.team_game_id : None,
        }

        self.parsers = {
            f.team_id        : cast_int,
            f.is_home        : is_home,
            f.pts            : cast_int,
            f.reb            : cast_int,
            f.oreb           : cast_int,
            f.dreb           : cast_int,
            f.ast            : cast_int,
            f.blk            : cast_int,
            f.stl            : cast_int,
            f.plus_minus     : cast_int,
            f.fouls          : cast_int,
            f.tov            : cast_int,
            f.minutes        : cast_int,
            f.fgm            : cast_int,
            f.fga            : cast_int,
            f.fg3m           : cast_int,
            f.fg3a           : cast_int,
            f.ftm            : cast_int,
            f.fta            : cast_int,
            f.won            : is_win,
            f.player_id      : cast_int,
            f.player_game_id : get_player_game_id,
            f.team_game_id   : get_team_game_id,
            f.game_date      : get_game_date,
            f.roster         : lambda k, v : []
        }
        return



class PlayerGameNode(BaseGameNode):

    def __init__(self, nba_data):
        BaseGameNode.__init__(self, nba_data)
        self.attrs.update({
            f.player_id      : 'PLAYER_ID',
            f.player_name    : 'PLAYER_NAME',
            f.player_game_id : None,
        })
        self.init_attrs(nba_data)
        return



class TeamGameNode(BaseGameNode):

    def __init__(self, nba_data):
        BaseGameNode.__init__(self, nba_data)
        self.attrs.update({
            f.roster : None,
        })
        self.init_attrs(nba_data)
        return

