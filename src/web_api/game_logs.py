import nba_py
from nba_py import league as nba_py_league

from database.tables.fields import Fields as f
from util.basic import identity, cast_int, is_home, is_win, get_player_game_id, get_team_game_id, get_season

nba_py.HAS_PANDAS = False

def get_player_game_logs(year):
    return [NBAPlayerGameLog(datum) for datum in _get_game_logs(year, 'P')]


def get_team_game_logs(year):
    return [NBATeamGameLog(datum) for datum in _get_game_logs(year, 'T')]


def _get_game_logs(year, player_or_team):
    season = get_season(year)
    return nba_py_league.GameLog(season=season, player_or_team=player_or_team).overall()


attrs = {
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

## Functions for transforming nba_data fields into ints and whatnot
transforms = {
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
    f.roster         : lambda k, v : []
}



class NBAPlayerGameLog():

    def __init__(self, nba_data):
        self.attrs = {
            f.player_id      : 'PLAYER_ID',
            f.player_name    : 'PLAYER_NAME',
            f.player_game_id : None,
        }
        self.attrs.update(attrs)
        for attr, nba_key in self.attrs.items():
            setattr(self, attr, transforms.get(attr, identity)(nba_data, nba_key))
        return



class NBATeamGameLog():

    def __init__(self, nba_data):
        self.attrs = {
            f.roster       : None,
        }
        self.attrs.update(attrs)
        for attr, nba_key in self.attrs.items():
            setattr(self, attr, transforms.get(attr, identity)(nba_data, nba_key))
        return

