import nba_py
from nba_py import team as nba_py_team

nba_py.HAS_PANDAS = False

"""
Returns a dict of <team_id, [player_ids]> pairs for every team as of today
"""
def get_all_current_rosters():
    team_ids = [int(team['id']) for team in nba_py.constants.TEAMS.values()]
    rstr = lambda tid : [int(p['PLAYER_ID']) for p in nba_py_team.TeamCommonRoster(tid).roster()]
    return { tid : rstr(tid) for tid in team_ids }
