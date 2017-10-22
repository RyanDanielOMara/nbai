#!env/bin/python
import argparse
import datetime
import logging

from util import database_util
from util.basic import log_call_stack

from web_api.api import get_player_game_nodes, get_team_game_nodes

now = datetime.datetime.utcnow()
CURRENT_SEASON_YEAR = now.year if now.month > 8 else now.year - 1


"""
Populates the database with player info and game info.
Given a range of [start_season, end_season), this populates
the Schedules, Players, Teams, PlayerGameLog, and TeamGameLog
collections with the appropriate data.

Does not add duplicates, so if this is run multiple times in succession
no data duplication errors will arise.
"""
@log_call_stack
def backfill_server(start_year, end_year, add_missing_player_bios, update_all_player_bios):

    ## Create all the teams (without active rosters)
    database_util.create_and_save_all_team_records()

    ## Create a dict to store PlayerRecords (for database efficiency)
    player_dict = {}

    ## For each year in the date range we want to fill:
    for year in range(start_year, end_year):

        ## Get all the PlayerGameLogs and TeamGameLogs
        player_game_nodes = get_player_game_nodes(year)
        team_game_nodes = get_team_game_nodes(year)

        ## Add all the Players from this season to the database
        database_util.create_and_save_all_player_records(player_game_nodes, year, player_dict)

        ## Add all the PlayerGameLogs from this season to the database
        database_util.create_and_save_all_player_game_log_records(player_game_nodes)

        ## Add all the TeamGameLogs from this season to the database
        team_game_rosters = database_util.get_team_game_rosters(player_game_nodes)
        database_util.create_and_save_all_team_game_log_records(team_game_nodes, team_game_rosters)

        ## Add all the Schedues from this season to the database
        database_util.create_and_save_all_schedule_records(team_game_nodes)

    ## Now, update current rosters and player biographical data
    database_util.update_rosters()
    database_util.update_short_player_bios()
    if add_missing_player_bios or update_all_player_bios:
        database_util.update_long_player_bios(update_all_player_bios)

    ## And add the most recent schedules
    database_util.create_and_save_2017_schedule_records()



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_year', type=int, default=2007, required=True)
    parser.add_argument('--end_year',   type=int, default=CURRENT_SEASON_YEAR, required=True)
    parser.add_argument('-a', '--add_missing_player_bios', action='store_true')
    parser.add_argument('-u', '--update_all_player_bios',  action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    backfill_server(
        start_year              = args.start_year,
        end_year                = args.end_year,
        add_missing_player_bios = args.add_missing_player_bios,
        update_all_player_bios  = args.update_all_player_bios
    )
