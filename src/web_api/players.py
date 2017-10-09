import nba_py

from nba_py import player as nba_py_player
from database.tables.fields import Fields as f
from util.basic import identity, cast_int, get_height, get_dob

nba_py.HAS_PANDAS = False



"""
Returns a list of ShortPlayerBios
"""
def get_all_short_player_bios():
    return [ShortPlayerBio(datum) for datum in nba_py_player.PlayerList().info()]



"""
Returns a single FullPlayerBio
"""
def get_full_player_bio(player_id):
    return FullPlayerBio(nba_py_player.PlayerSummary(player_id).info()[0])



class ShortPlayerBio:

    attrs = {
        f.player_id   : 'PERSON_ID',
        f.player_name : 'DISPLAY_FIRST_LAST',
        f.first_year  : 'FROM_YEAR',
    }

    transforms = {
        f.player_id  : cast_int,
        f.first_year : cast_int,
    }

    def __init__(self, nba_data):
        for attr, nba_key in self.attrs.items():
            setattr(self, attr, self.transforms.get(attr, identity)(nba_data, nba_key))
        return



class FullPlayerBio:

    attrs = {
        f.player_id   : 'PERSON_ID',
        f.player_name : 'DISPLAY_FIRST_LAST',
        f.first_year  : 'FROM_YEAR',
        f.last_year   : 'TO_YEAR',
        f.height      : 'HEIGHT',
        f.weight      : 'WEIGHT',
        f.dob         : 'BIRTHDATE',
        f.country     : 'COUNTRY',
        f.exp         : 'SEASON_EXP',
        f.position    : 'POSITION',
        f.jersey      : 'JERSEY',
    }

    transforms = {
        f.player_id   : cast_int,
        f.first_year  : cast_int,
        f.last_year   : cast_int,
        f.height      : get_height,
        f.weight      : cast_int,
        f.dob         : get_dob,
        f.exp         : cast_int,
    }

    def __init__(self, nba_data):
        for attr, nba_key in self.attrs.items():
            setattr(self, attr, self.transforms.get(attr, identity)(nba_data, nba_key))
        return

