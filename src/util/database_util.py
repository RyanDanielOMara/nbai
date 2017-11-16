import logging
import nba_py

from pymongo import MongoClient

from util.basic import log_call_stack
from web_api.api import get_all_rosters, get_all_short_player_bios, get_long_player_bio, get_2017_schedule_nodes
from database.connection import DATABASE_NAME, connection
from database.tables.fields import Fields as f
from database.tables.league.players import PlayerRecord
from database.tables.league.player_game_logs import PlayerGameLogRecord
from database.tables.league.teams import TeamRecord
from database.tables.league.team_game_logs import TeamGameLogRecord
from database.tables.league.schedules import ScheduleRecord
from database.tables.league.player_season_stats import PlayerSeasonStatsRecord



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
        if player_rec.games_dict.get(year_str):
            player_rec.games_dict[year_str] = sorted(set(player_rec.games_dict[year_str]))
            player_rec.save()
            logging.info('SAVED PLAYER to database: {}'.format(player_rec.player_id))
    return



"""
Creates and saves all nonexistent PlayerGameLogRecords, if not present in the database
"""
def create_and_save_all_player_game_log_records(player_game_logs):
    _create_and_save_game_logs(player_game_logs, f.player_game_id, PlayerGameLogRecord.__collection__)



"""
Creates and saves all nonexistent TeamGameLogRecords, if not present in the database
"""
def create_and_save_all_team_game_log_records(team_game_logs, team_game_rosters):
    _create_and_save_game_logs(team_game_logs, f.team_game_id, TeamGameLogRecord.__collection__, team_game_rosters)



"""
Genericized form of create_and_save_all_XXX_game_log_records()
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

    num_saved_records = 0
    if batch:
        saved_records = game_log_table.insert(batch)
        num_saved_records = len(saved_records)

    logging.info("CREATED/SAVED this many {}s:      {}".format(primary_key, num_saved_records))
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
def update_rosters(year):

    ## Get all rosters
    rosters = get_all_rosters(year)


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
                player_rec.save()

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
Updates some player biographical info.

This is fast.  Sends one HTTP request and gets every player's
name, player_id, and other fields.
"""
@log_call_stack
def update_short_player_bios():

    ## First, get all the player info from the web api
    bio_dict = { node.player_id : node for node in get_all_short_player_bios() }

    ## Now, for every player in the db, update their short bio
    for player_rec in connection.PlayerRecord.find():

        ## Get this player's bio
        bio = bio_dict[player_rec.player_id]

        ## Set all the fields
        for field in bio.attrs:
            setattr(player_rec, field, getattr(bio, field))

        ## Save this record
        player_rec.save()
    return



"""
Updates all player biographical info.

This is SLOW.  Each player requires a unique HTTP request
to retrieve their data.  This only needs to be run once
every so often, such as at the end of a season or during
initial database setup.
"""
@log_call_stack
def update_long_player_bios(update_all_player_bios):

    counter_for_logging = 0
    for player_rec in connection.PlayerRecord.find():

        ## If this player doesn't have their full bio,
        ## or if you want to update it regardless, then do so:
        if update_all_player_bios or not player_rec.has_bio:
            bio = get_long_player_bio(player_rec.player_id)

            ## Set all the fields
            for field in bio.attrs:
                setattr(player_rec, field, getattr(bio, field))
                player_rec.has_bio = True
            player_rec.save()

            ## Logging purposes only
            counter_for_logging += 1
            if counter_for_logging % 50 == 0:
                logging.info('Updated {} Player bios'.format(counter_for_logging))
    logging.info('Updated {} Player bios in total'.format(counter_for_logging))
    return



"""
Creates and saves all nonexistent ScheduleRecords, if not present in the database
"""
def create_and_save_all_schedule_records(team_game_nodes):

    ## Create a dict of (team_game_id, game_date) pairs
    scheds = { node.team_game_id : node for node in team_game_nodes }
    game_dates = list(set([node.game_date for node in team_game_nodes]))

    ## Query the database for every ScheduleRecord
    sched_table = getattr(getattr(MongoClient(), DATABASE_NAME), ScheduleRecord.__collection__)
    query = { f.game_date : { '$in' : game_dates } }
    previously_saved_records = { rec[f.team_game_id] : rec for rec in sched_table.find(query) }

    ## Create ScheduleRecords for all games not in the database
    batch = [_get_schedule_record(node, True)
             for node in scheds.values()
             if node.team_game_id not in previously_saved_records]

    ## Save all new records
    num_saved_records = 0
    if len(batch) > 0:
        num_saved_records = len(sched_table.insert(batch))
    logging.info('Updated {} ScheduleRecords.'.format(num_saved_records))
    return



def _get_schedule_record(node, game_log_saved):
    rec = connection.ScheduleRecord()
    rec.game_date    = node.game_date
    rec.game_id      = node.game_id
    rec.team_id      = node.team_id
    rec.team_game_id = node.team_game_id
    rec.is_home      = node.is_home
    rec.game_log_saved = game_log_saved
    return rec



@log_call_stack
def create_and_save_2017_schedule_records(skip_preseason=True,
                                          skip_regular_season=False,
                                          skip_postseason=True):

    ## Get all the ScheduleNodes for this year
    schedule_nodes = get_2017_schedule_nodes(skip_preseason, skip_regular_season, skip_postseason)

    ## Get a list of game_ids from these nodes
    team_game_ids = [node.team_game_id for node in schedule_nodes]

    ## Query the database for every 2017 ScheduleRecord
    sched_table = getattr(getattr(MongoClient(), DATABASE_NAME), ScheduleRecord.__collection__)
    query = { f.team_game_id : { '$in' : team_game_ids } }
    previously_saved_records = { rec[f.team_game_id] : rec for rec in sched_table.find(query) }

    ## Create ScheduleRecords for all games not in the database
    batch = [_get_schedule_record(node, False) for node in schedule_nodes
             if node.team_game_id not in previously_saved_records]

    ## Save all new records
    num_saved_records = 0
    if len(batch) > 0:
        num_saved_records = len(sched_table.insert(batch))
    logging.info('Updated {} ScheduleRecords.'.format(num_saved_records))



"""
Creates a PlayerSeasonStatsRecord from a list of PlayerGameNodes.
Assumes that the nodes in pg_nodes all have the same player_id.
"""
def _get_player_season_stats_record(player_id, pg_nodes, season):

    ## Create a PlayerSeasonStatsRecord object
    rec = connection.PlayerSeasonStatsRecord()

    ## Get a list of all the statistical attributes
    stat_attrs = [f.pts, f.reb, f.oreb, f.dreb, f.ast, f.blk, f.stl,
                  f.plus_minus, f.fouls, f.tov, f.minutes, f.fgm,
                  f.fga, f.fg3m, f.fg3a, f.ftm, f.fta, f.won]

    ## Set the records non-statistical fields
    rec.player_id = player_id
    rec.season = season
    rec.games_played = len(pg_nodes)

    ## And, for each player_game_node:
    for node in pg_nodes:

        ## Set all the statistical attributes
        for field in stat_attrs:

            ## Set the rec's default value (if necessary)
            if getattr(rec, field) is None:
                setattr(rec, field, 0)

            ## And increment the field
            setattr(rec, field, getattr(rec, field) + getattr(node, field))

    ## Return the record
    return rec



"""
Creates and saves all nonexistent PlayerSeasonStatsRecords, if not present in the database
"""
def create_and_save_all_player_season_stats_records(player_game_nodes, season):

    ## Create a dict of {player_id : [player_game_node]} pairs
    player_dict = {}
    for node in player_game_nodes:
        player_dict.setdefault(node.player_id, []).append(node)

    ## Create a list of records representing these nodes
    records_we_might_save = [_get_player_season_stats_record(player_id, nodes, season)
                             for player_id, nodes in player_dict.items()]

    ## Get the table we're saving to
    table_name = PlayerSeasonStatsRecord.__collection__
    player_season_stats_table = getattr(getattr(MongoClient(), DATABASE_NAME), table_name)

    ## Query the database for records already in there
    player_id_query = { f.player_id : { '$in' : player_dict.keys() } }
    season_query = { f.season : season }
    query = { '$and' : [ player_id_query, season_query ] }
    previously_saved_records = { rec[f.player_id] : rec for rec in
                                 player_season_stats_table.find(query) }

    ## Get the records to save
    insert_count = 0
    update_count = 0
    bulk_operation = player_season_stats_table.initialize_ordered_bulk_op()
    for rec in records_we_might_save:

        ## If this player is not in the database
        if rec.player_id not in previously_saved_records:
            bulk_operation.insert(rec)
            insert_count += 1

        ## Otherwise, if this player already exists for this year,
        ## but this record is newer, update it
        elif rec.player_id in previously_saved_records \
        and rec.games_played > previously_saved_records[rec.player_id][f.games_played]:
            old_id = previously_saved_records[rec.player_id]['_id']
            bulk_operation.find({'_id' : old_id}).update({'$set' : rec})
            update_count += 1

    ## Save all of these records
    if insert_count > 0 or update_count > 0:
        saved_records = bulk_operation.execute()
        insert_count = saved_records['nInserted']
        update_count = saved_records['nModified']

    logging.info("INSERTED this many {} PlayerSeasonStatRecords: {}".format(season, insert_count))
    logging.info("UPDATED  this many {} PlayerSeasonStatRecords: {}".format(season, update_count))
    return

