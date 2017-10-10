import nba_py
from nba_py import league as nba_py_league
from nba_py import player as nba_py_player
from nba_py import team as nba_py_team
from nba_py.constants import TEAMS

from web_api.nodes.gamenodes import PlayerGameNode, TeamGameNode
from web_api.nodes.rosternodes import RosterNode
from web_api.nodes.playernodes import ShortPlayerBioNode, LongPlayerBioNode

nba_py.HAS_PANDAS = False



"""
Returns a list of ShortPlayerBioNodes
"""
def get_all_short_player_bios():
    return [ShortPlayerBioNode(datum) for datum in nba_py_player.PlayerList().info()]



"""
Returns a single FullPlayerBioNode
"""
def get_long_player_bio(player_id):
    return LongPlayerBioNode(nba_py_player.PlayerSummary(player_id).info()[0])



"""
Returns a dict of <team_id, RosterNode> pairs for every team as of today
"""
def get_all_current_rosters():
    team_ids = [int(team['id']) for team in TEAMS.values()]
    nba_data = lambda team_id : nba_py_team.TeamCommonRoster(team_id).roster()
    return { tid : RosterNode(nba_data(tid), tid) for tid in team_ids }



"""
Returns a list of PlayerGameNodes for a given season
"""
def get_player_game_nodes(year):
    return [PlayerGameNode(datum) for datum in get_gamelog_json(year, 'P')]



"""
Returns a list of TeamGameNodes for a given season
"""
def get_team_game_nodes(year):
    return [TeamGameNode(datum) for datum in get_gamelog_json(year, 'T')]



"""
Returns a JSON node containing player or team game logs from stats.nba.com
"""
def get_gamelog_json(year, player_or_team):
    season = '{}-{}'.format(year, str(year+1)[2:])
    return nba_py_league.GameLog(season=season, player_or_team=player_or_team).overall()

