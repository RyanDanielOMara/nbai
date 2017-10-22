import json
import requests

import nba_py
from nba_py import league as nba_py_league
from nba_py import player as nba_py_player
from nba_py import team as nba_py_team
from nba_py.constants import TEAMS

from web_api.parsers import get_game_date
from web_api.nodes.gamenodes import PlayerGameNode, TeamGameNode
from web_api.nodes.rosternodes import RosterNode
from web_api.nodes.playernodes import ShortPlayerBioNode, LongPlayerBioNode
from web_api.nodes.schedulenodes import ScheduleNode

nba_py.HAS_PANDAS = False



"""
Returns a list of ShortPlayerBioNodes
"""
def get_all_short_player_bios():
    return [ShortPlayerBioNode(datum) for datum in nba_py_player.PlayerList(only_current=0).info()]



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



"""
Returns a list of 2017 schedule nodes
"""
def get_2017_schedule_nodes(skip_preseason, skip_regular_season, skip_postseason):

    is_preseason      = lambda game_node : game_node['gid'].startswith('001')
    is_regular_season = lambda game_node : game_node['gid'].startswith('002')
    is_postseason     = lambda game_node : game_node['gid'].startswith('004')

    nodes = []
    url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule_week.json'
    nba_data = json.loads(requests.get(url).text)
    for month_data in nba_data['lscd']:
        for game_data in month_data['mscd']['g']:
            if skip_preseason and is_preseason(game_data):
                    continue
            if skip_regular_season and is_regular_season(game_data):
                    continue
            if skip_postseason and is_postseason(game_data):
                    continue
            for (team, is_team_at_home) in [('h', True), ('v', False)]:
                node = ScheduleNode(game_data)
                node.game_date    = get_game_date(game_data, 'gdte')
                node.game_id      = game_data['gid']
                node.team_id      = int(game_data[team]['tid'])
                node.team_game_id = str(str(node.team_id) + node.game_id)
                node.is_home      = is_team_at_home
                nodes.append(node)
    return nodes

