from database.connection import connection
from database.tables._base import DatabaseRecord
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s

TABLE_NAME = 'player_season_stats'


@connection.register
class PlayerSeasonStatsRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.player_id    : s.player_id, 
        f.season       : s.season,
        f.pts          : s.pts,
        f.reb          : s.reb,
        f.oreb         : s.oreb,
        f.dreb         : s.dreb,
        f.ast          : s.ast,
        f.blk          : s.blk,
        f.stl          : s.stl,
        f.plus_minus   : s.plus_minus,
        f.fouls        : s.fouls,
        f.tov          : s.tov,
        f.minutes      : s.minutes,
        f.fgm          : s.fgm,
        f.fga          : s.fga,
        f.fg3m         : s.fg3m,
        f.fg3a         : s.fg3a,
        f.ftm          : s.ftm,
        f.fta          : s.fta,
        f.won          : s.won,
        f.games_played : s.games_played,
    }

    indexes = [
        {
            'fields' : [f.player_id],
            'unique' : False
        }
    ]

    required_fields = [
        f.player_id, 
        f.season,
        f.pts,
        f.reb,
        f.oreb,
        f.dreb,
        f.ast,
        f.blk,
        f.stl,
        f.plus_minus,
        f.fouls,
        f.tov,
        f.minutes,
        f.fgm,
        f.fga,
        f.fg3m,
        f.fg3a,
        f.ftm,
        f.fta,
        f.won,
        f.games_played,
    ]

    default_values = {
    }

