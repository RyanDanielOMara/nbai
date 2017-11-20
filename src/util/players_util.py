import string
import math
import operator
import unicodedata
import pymongo

from datetime import date, datetime
from database.connection import DATABASE_NAME, connection
from database.tables.fields import Fields as f
from nba_py import team as nba_team
from nba_py import player as nba_player
from database.tables.league.players import PlayerRecord
from database.tables.league.player_prediction import PlayerPredictionRecord
from database.tables.league.player_season_stats import PlayerSeasonStatsRecord



"""
Attemps to create a player dict containing information to be rendered.

Connects to the database and searches for a player based on a playerid passed
in from the path.  If the player cannot be located in the database or is no
longer active, we will return none and the server will return a 404 status code.

If the player is found and is active, call functions to format position and
height and to calculate age from the player dob.

Returns the player dict.
"""
def extract_player_info(playerid):
    try:
        player = connection.NBAI.players.find_one({f.player_id : int(playerid)},
         {f.player_id    : 1,
         f.player_name   : 1,
         f.height        : 1,
         f.weight        : 1,
         f.dob           : 1,
         f.position      : 1,
         f.jersey        : 1,
         f.last_year     : 1,
         f.team_id       : 1,
         f.pre_nba       : 1,
         f.draft_overall : 1,
         f.draft_year    : 1,
         '_id'           : 0})
    except:
        return None

    if not player or player[f.last_year] != date.today().year :
        return None
    player[f.team_abbr]     = get_player_team(player[f.team_id])
    player[f.position]      = get_player_position(player[f.position])
    player[f.height]        = get_player_height(player[f.height])
    player['age']           = get_player_age(player[f.dob])
    player['draft']         = get_draft_pick(player[f.draft_year], player[f.draft_overall])

    return player


"""
Given a player position from the database, formats the position for display.

If the player has a position in the database, we must first convert the string
from unicode to ascii to call translate, and we then remove all lowercase
letters so that Forward => F, Guard-Forward => G-F, etc...

Returns the position if there is one, otherwise returns an empty string.
"""
def get_player_position(position):
    if position:
        unicode_to_string  = unicodedata.normalize('NFKD', position).encode('ascii','ignore')
        return unicode_to_string.translate(None,string.ascii_lowercase)
    return ''


"""
Given a player height from the database in inches, formats it for display.

Returns height in feet and inches if the player has a height in the database,
returns an empty string otherwise.
"""
def get_player_height(height):
        return str(int(math.floor(int(height)/12))) + "'" + str(int(height)%12) + '"' if height else ''


"""
Given a player date of birth from the database, calculates the player's age.

Returns the player's age if a dob exists, returns an empty string otherwise.
"""
def get_player_age(dob):
        if(dob):
            dob_year, dob_month, dob_day = [int(x) for x in dob.split('-')]
            today = date.today()
            return today.year - dob_year - ((today.month, today.day) < (dob_month, dob_day))
        else:
            return ''


"""
Given a team id, retrieves the team abbreviation.

Returns a string - team abbreviation if found, empty string otherwise.
"""
def get_player_team(teamid):
    try:
        team_abbr = connection.NBAI.teams.find_one({f.team_id : int(teamid)}, {f.team_abbr : 1, '_id' : 0})[f.team_abbr]
        return team_abbr
    except:
        return ''


"""
Given a draft year and overall pick, format the pick string.

Returns a string representing a player's draft position.
"""
def get_draft_pick(draft_year, draft_pick):
    if draft_pick == 'Undrafted':
        return draft_pick
    draft_pick = draft_pick + 'st' if draft_pick == '1' else draft_pick + 'th'
    return '{} : {} overall'.format(draft_year, draft_pick)


"""
Given a year as an int

Return a list of lists of players and their corresponding playerid.
"""
def get_list_of_all_players(year):
    players = connection.PlayerRecord.find({f.last_year : year})
    return [(player_item.player_id, player_item.player_name) for player_item in players]


"""
Loads 3 players from teams playing on the current day.  The 3 players that are
loaded are the 3 players who played the most minutes for a given team in their
previous game.

Returns a list of players, position, value, opponent.
"""
def load_todays_players():
    todays_date = datetime.strftime(datetime.now(), '%Y%m%d')
    games = {}
    output = []

    todays_games = connection.NBAI.schedules.find({f.game_date : todays_date})
    for game in todays_games:
        team_abbr = connection.NBAI.teams.find_one({f.team_id : int(game[f.team_id])}, {f.team_abbr : 1, '_id' : 0})[f.team_abbr]
        game_id = game[f.game_id]
        if game_id not in games:
            games[game_id] = {}
            games[game_id]['teams'] = []
        games[game_id]['teams'].append({team_abbr : None})

    for game_id, game in games.items():
        for team in game['teams']:
            team1 = game['teams'][0].keys()[0]
            team2 = game['teams'][1].keys()[0]
            opp = team1 if team.keys()[0] == team2 else team2

            team_abbr = team.items()[0][0]

            most_recent_game        = connection.NBAI.team_game_logs.find({f.team_abbr : team_abbr}).sort(f.game_date, pymongo.DESCENDING).limit(1)[0]
            most_recent_game_id     = most_recent_game[f.game_id]
            most_recent_game_roster = most_recent_game[f.roster]

            player_minutes_in_last_game = {player_id : (
                connection.NBAI.player_game_logs.find_one(
                {f.player_id : player_id,
                f.game_id : most_recent_game_id})['minutes'])
                for player_id in most_recent_game_roster}

            sorted_players_by_minutes_played = sorted(
                player_minutes_in_last_game.items(),
                key=operator.itemgetter(1),
                reverse=True
            )

            roster_ids = [x[0] for x in sorted_players_by_minutes_played[:6]]

            for player in roster_ids:
                player_item = extract_player_info(int(player))
                if(player_item):
                    output.append([[player_item[f.player_name], player_item[f.player_id]], team_abbr, player_item[f.position], opp, game_id])
                else:
                    continue
    return output


"""
Loads todays teams playing in games from the database.

Returns a list team abbreviations.
"""
def get_todays_games():
    todays_date = datetime.strftime(datetime.now(), '%Y%m%d')
    games = []

    todays_games = connection.NBAI.schedules.find({f.game_date : todays_date})
    for game in todays_games:
        team_abbr = connection.NBAI.teams.find_one({f.team_id : int(game[f.team_id])}, {f.team_abbr : 1, '_id' : 0})[f.team_abbr]
        games.append(team_abbr)
    return games


"""
Gets projected player fantasy scores and updates the front page player list

Returns a tuple of an updated player list and a list of top 3 valued players.
"""
def get_player_scores(players):
    player_values = {}
    for player in players:
        player_name, player_id, team_abbr, opp, game_id = player[0][0], player[0][1], player[1], player[3], player[4]
        opp_id   = connection.NBAI.teams.find_one({f.team_abbr : team_abbr}, {f.team_id : 1, '_id' : 0})['team_id']
        print('Getting opponent team ID...')

        ftsy_prj, value = calculate_fantasy_points(player_id, opp_id)
        value = min(value, 1.5)

        rec = connection.PlayerPredictionRecord()
        rec.player_id = player_id
        rec.game_id    = game_id
        rec.team_abbr  = team_abbr
        rec.prediction = ftsy_prj
        rec.save()

        print('Player: {}'.format(player_name))
        print('    Playing against: {}'.format(team_abbr))
        print('    Projected points:  {}'.format(ftsy_prj))

        player.append(int(ftsy_prj))
        if ftsy_prj > 25 and value > 1.0:
            ten_game_avg = ftsy_prj/value
            player_values[value] = [int(ftsy_prj), int(ten_game_avg), int(ftsy_prj)-int(ten_game_avg), player_id, player_name]
        del player[4]

    sorted_player_values = sorted(player_values.items(), key=operator.itemgetter(0), reverse=True)
    player_values = [x[1] for x in sorted_player_values[:3]]
    return (players, player_values)


"""
Retrieves and makes some adjustments to our player projections based on recent
performance of a player.  Calculates a player's value based on their projected
points on a given night against their recent 10-game average.

Returns a tuple of the projected fantasy points of a player and their value.
"""
def calculate_fantasy_points(player_id, opp_team_id):
    ftsy_prj = nba_team.TeamVsPlayer(opp_team_id, player_id, season='2017-18').vs_player_overall()
    ftsy_prj = ftsy_prj[0]['NBA_FANTASY_PTS'] if len(ftsy_prj) else 0

    ftsy_pts_last_5 = nba_player.PlayerLastNGamesSplits(player_id).last5()
    if not len(ftsy_pts_last_5):
        ftsy_pts_last_5 = 0
        ftsy_pts_last_10 = 0
    else:
        ftsy_pts_last_5 = ftsy_pts_last_5[0]['NBA_FANTASY_PTS']

        ftsy_pts_last_10 = nba_player.PlayerLastNGamesSplits(player_id).last10()
        ftsy_pts_last_10 = ftsy_pts_last_10[0]['NBA_FANTASY_PTS'] if len(ftsy_pts_last_10) else 0

    recent_form = 1 if (ftsy_pts_last_10 == 0 or ftsy_pts_last_5 == 0) else (ftsy_pts_last_5/ftsy_pts_last_10)

    recent_form = min(max(.85, recent_form), 1.15)
    ftsy_prj = round(ftsy_prj * recent_form, 1)
    value = ftsy_prj/ftsy_pts_last_10 if ftsy_pts_last_10 > 0 else 1
    return (ftsy_prj, value)


"""
Given a player_id, this will return a list containig career/seasonal stats.

Returns [columns, career_stats, season_stats]
'columns' is a list of the stat names in the order they appear in the career/season lists
'career_stats' is a list of stats for the players complete career
'season_stats' is a list containing lists of season stats.

Both career_stats and the lists inside season_stats are formatted like so:
[year, games_played, minutes, points, fgm, fga, ... ]
"""
def get_player_season_stats(player_id):

    ## Get the player from the database
    query = { f.player_id : int(player_id) }
    player_record_cursor = connection.PlayerSeasonStatsRecord.find(query)

    columns = [
        f.season,
        f.games_played,
        f.minutes,
        f.pts,
        f.fgm,
        f.fga,
        "fg%",
        f.fg3m,
        f.fg3a,
        "3p%",
        f.ftm,
        f.fta,
        "ft%",
        f.oreb,
        f.dreb,
        f.reb,
        f.ast,
        f.tov,
        f.stl,
        f.blk,
        f.fouls,
        f.plus_minus,
    ]

    ## Create placeholders for the seasonal/career stats
    season_stats = []
    career_stats_dict = { col : 0 for col in columns }

    ## Sort the PlayerSeasonStatRecords by year descending
    player_record_cursor = sorted(player_record_cursor, key=lambda rec : rec.season, reverse=True)

    ## For each record
    for rec in player_record_cursor:

        this_season = []

        ## Iterate through the stat columns
        for col in columns:

            ## If this column represents a percentage:
            if col == 'fg%':
                value = round(100.0 * rec.fgm / rec.fga , 1) if rec.fga else '-'
            elif col == '3p%':
                value = round(100.0 * rec.fg3m / rec.fg3a, 1) if rec.fg3a else '-'
            elif col == 'ft%':
                value = round(100.0 * rec.ftm / rec.fta, 1) if rec.fta else '-'

            ## Else, if this header is one that doesn't get normalized:
            elif col in [ f.games_played, f.season ]:
                value = getattr(rec, col)
                career_stats_dict[col] += value

            ## Otherwise, get this stat and normalize it (per game)
            else:
                value = round(1.0 * getattr(rec, col) / rec.games_played, 1) if rec.games_played else 0
                career_stats_dict[col] += getattr(rec, col)

            ## Add this value to this season
            this_season.append(value)

        ## Add this season to the season_stats
        season_stats.append(this_season)

    ## Now, build the career stats
    csd = career_stats_dict
    if csd[f.games_played]:
        career_stats = [round(1.0 * csd[col] / csd[f.games_played], 1) for col in columns]
    else:
        career_stats = ['-' for col in columns]
    ## Fix the stats that shouldn't be normalized
    season_index = 0
    games_played_index = 1
    fg_pct_idx = 6
    fg3_pct_idx = 9
    ft_pct_idx = 12
    career_stats[fg_pct_idx]  = round(100.0 * csd[f.fgm]  / csd[f.fga],  1) if csd[f.fga]  else '-'
    career_stats[fg3_pct_idx] = round(100.0 * csd[f.fg3m] / csd[f.fg3a], 1) if csd[f.fg3a] else '-'
    career_stats[ft_pct_idx]  = round(100.0 * csd[f.ftm]  / csd[f.fta],  1) if csd[f.fta]  else '-'
    career_stats[games_played_index] = csd[f.games_played]
    career_stats[season_index] = "Career"

    for i in range(len(columns)):
        if i == 1:
            columns[i] = 'GP'
        elif i == 2:
            columns[i] = 'MIN'
        elif i == 21:
            columns[i] = '+/-'
        else:
            columns[i] = columns[i].replace('_', ' ').upper()

    return [columns, career_stats, season_stats]
