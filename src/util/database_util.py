import logging
import nba_py

from pymongo import MongoClient

from util.basic import log_call_stack
from web_api.api import get_all_current_rosters, get_all_short_player_bios, get_long_player_bio
from database.connection import DATABASE_NAME, connection
from database.tables.fields import Fields as f
from database.tables.league.players import PlayerRecord
from database.tables.league.player_game_logs import PlayerGameLogRecord
from database.tables.league.teams import TeamRecord
from database.tables.league.team_game_logs import TeamGameLogRecord
from database.tables.league.schedules import ScheduleRecord



"""
Adds each team to our database (if not present).

Does not set/update rosters
"""
def create_and_save_all_team_records():

    for team_dict in nba_py.constants.TEAMS.values():

        ## Get relevant info
        team_id = int(team_dict['id'])
        team_abbr = team_dict['abbr']

        ## Check to see if this team exists in our db
        query = { f.team_id : team_id }
        result = connection.TeamRecord.one(query)

        ## If the team exists, do nothing
        if result is not None:
            logging.info("TEAM exists in database: {}".format(team_abbr))

        ## Otherwise, create and persist the team in the db
        else:
            logging.info("TEAM didn't exist: {}".format(team_abbr))
            create_and_save_one_team(team_dict)
    return



"""
Adds one team to the database.
Does not set roster, games, or query stats.nba.com
"""
@log_call_stack
def create_and_save_one_team(team_dict):
    team_rec = connection.TeamRecord()
    team_rec.team_id    = int(team_dict['id'])
    team_rec.team_name  = '{} {}'.format(team_dict['city'], team_dict['name'])
    team_rec.team_abbr  = team_dict['abbr']
    team_rec.division   = team_dict['division']
    team_rec.conference = team_dict['conference']
    team_rec.color      = team_dict['color']
    team_rec.colors     = team_dict['colors']
    team_rec.roster     = []
    team_rec.games_dict = {}
    team_rec.save()
    logging.info('SAVED TEAM to database: {}'.format(team_rec.team_abbr))
    return



"""
Creates and saves all PlayerRecords for a given season.

If given a dict (optional), this will first search the dict
for a given player (to reduce queries to the database when
populating multiple seasons).

Does not update biographical info.
Does not update player_name (this is intentional).
"""
def create_and_save_all_player_records(player_game_logs, year, player_dict=None):

    ## Create an empty dictionary if none exists
    if player_dict is None:
        player_dict = {}

    ## Get the year as a string
    year_str = str(year)

    ## For each player in the game log:
    for pg in player_game_logs:

        ## Get relevant info
        player_name = pg.player_name
        player_id = pg.player_id
        game_id = pg.game_id
        
        ## Grab this player from the dictionary
        player_rec = player_dict.get(player_id)
        
        ## If this player is not in the dictionary:
        if player_rec is None:
        
            ## Try to retrieve them from the database
            query = { f.player_id : player_id }
            player_rec = connection.PlayerRecord.one(query)
        
            ## If they are not in the database, create a record
            if player_rec is None:
                player_rec = connection.PlayerRecord()
                player_rec.player_id = player_id
                logging.info("PLAYER didn't exist.  CREATED: {}".format(player_name))
            else:
                logging.info("PLAYER exists in database: {}".format(player_name))
            
            ## Put them in the dictionary
            player_dict[player_id] = player_rec
        
        ## Update this player's list of games
        player_rec.games_dict.setdefault(year_str, []).append(game_id)

    ## Sort each PlayerRecord's list of games
    ## and save this PlayerRecord into the database
    for player_rec in player_dict.values():
        player_rec.games_dict[year_str] = sorted(set(player_rec.games_dict.get(year_str, [])))
        player_rec.save()
        logging.info('SAVED PLAYER to database: {}'.format(player_rec.player_id))
    return



"""
Creates and saves all nonexistient PlayerGameLogRecords, if not present
"""
def create_and_save_all_player_game_log_records(player_game_logs):
    _create_and_save_game_logs(player_game_logs, f.player_game_id, PlayerGameLogRecord.__collection__)



"""
Creates and saves all nonexistient TeamGameLogRecords, if not present
"""
def create_and_save_all_team_game_log_records(team_game_logs, team_game_rosters):
    _create_and_save_game_logs(team_game_logs, f.team_game_id, TeamGameLogRecord.__collection__, team_game_rosters)



"""
Genericized form of	create_and_save_all_XXX_game_log_records()
"""
def _create_and_save_game_logs(game_logs, primary_key, table_name, team_game_rosters=None):

    ## Check if any of the records we're trying to save
    ## are already in the database (via a batch query)
    game_log_dict = { getattr(game_log, primary_key) : game_log for game_log in game_logs }
    game_log_table = getattr(getattr(MongoClient(), DATABASE_NAME), table_name)
    query = { primary_key : { '$in' : game_log_dict.keys() } }
    previously_saved_records = { log[primary_key] : log for log in game_log_table.find(query) }

    ## For logging purposes only
    num_prev_recs = len(previously_saved_records)
    num_recs_needed = len(game_log_dict) - num_prev_recs
    logging.info("Database contained this many {}s: {}".format(primary_key, num_prev_recs))
    logging.info("Need to create this many {}s:     {}".format(primary_key, num_recs_needed))

    ## If all of these GameLogs are already in the database, exit
    if num_recs_needed == 0:
        return

    ## Otherwise, create any object that's not already here
    batch = [_get_game_log_record(log, primary_key, team_game_rosters)
             for idee, log in game_log_dict.items()
             if idee not in previously_saved_records]
    saved_records = game_log_table.insert(batch)
    logging.info("CREATED/SAVED this many {}s:      {}".format(primary_key, len(saved_records)))
    return



"""
Creates a GameRecord from a GameLog.  Sets the roster if applicable.
"""
def _get_game_log_record(game_log, primary_key, team_game_rosters=None):

    if primary_key == f.player_game_id:
        rec = connection.PlayerGameLogRecord()
    elif primary_key == f.team_game_id:
        rec = connection.TeamGameLogRecord()
    else:
        raise ValueError('Improper primary_key: {}'.format(primary_key))

    ## Set all the fields
    for field in game_log.attrs:
        setattr(rec, field, getattr(game_log, field))

    ## Set the rosters (if any were passed in)
    if team_game_rosters:
        rec.roster = team_game_rosters.get(game_log.team_game_id, [])

    ## Return the GameRecord
    return rec



"""
Returns a dict of <team_game_id : [player_id]> pairs.
These rosters are the rosters for a specific team_game_id,
not the current active rosters.
"""
def get_team_game_rosters(player_game_logs):
    team_game_rosters = {}
    for game_log in player_game_logs:
        team_game_rosters.setdefault(game_log.team_game_id, []).append(game_log.player_id)
    return team_game_rosters



"""
Updates the current roster of every team.
Also updates the player's team data, if they were dropped or added.
"""
@log_call_stack
def update_rosters():

    ## Get all rosters
    rosters = get_all_current_rosters()
    

    ## For each team in the league
    for team_rec in connection.TeamRecord.find():

        team_id = team_rec.team_id
        old_roster = team_rec.roster
        new_roster = rosters[team_id].roster

        ## Set the teams new roster
        team_rec.roster = new_roster

        ## See who was cut and who was picked up
        dropped = set(old_roster) - set(new_roster)
        added   = set(new_roster) - set(old_roster)
        logging.info('{} dropped {} players since last db update'.format(team_rec.team_abbr, len(dropped)))
        logging.info('{} added {} players since last db update'.format(team_rec.team_abbr, len(added)))

        ## Update the current team for all dropped players
        for player_id in dropped:
            query = { f.player_id : player_id }
            player_rec = connection.PlayerRecord.one(query)
            if player_rec.team_id == team_id:
                player_rec.team_id = None
                player.save()

        ## Update the current team for all added players
        for player_id in added:
            query = { f.player_id : player_id }
            player_rec = connection.PlayerRecord.one(query)
            if player_rec is None:
                player_rec = connection.PlayerRecord()
                player_rec.player_id = player_id
            player_rec.team_id = team_id
            player_rec.save()
            
        ## Save the team
        team_rec.save()
    return



"""
Updates player biographical info.

This is SLOW.  Each player requires a unique HTTP request
to retrieve their data.  This only needs to be run once
every so often, such as at the end of a season or during
initial database setup.
"""
@log_call_stack
def update_player_bios(full_bio=False, reupdate_full_bios=False):

    ## First, update name and draft year of active players
    for bio in get_all_short_player_bios():
        query = { f.player_id : bio.player_id }
        player_rec = connection.PlayerRecord.one(query)
        if player_rec is None:
            player_rec = connection.PlayerRecord()
            player_rec.player_id = bio.player_id
        player_rec.player_name = bio.player_name
        player_rec.first_year = bio.first_year
        player_rec.save()

    ## Now, update as much biographical info as you can.
    if full_bio:
        counter_for_logging = 0
        for player_rec in connection.PlayerRecord.find():

            ## If this player doesn't have their full bio,
            ## or if you want to update it regardless, then do so:
            if reupdate_full_bios or not player_rec.has_bio:
                bio = get_long_player_bio(player_rec.player_id)

                ## Set all the fields
                for field in bio.attrs:
                    setattr(player_rec, field, getattr(bio, field))

                ## Logging purposes only
                counter_for_logging += 1
                if counter_for_logging % 50 == 0:
                    logging.info('Updated {} Player bios'.format(counter_for_logging))
        logging.info('Updated {} Player bios in total'.format(counter_for_logging))



