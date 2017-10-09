from database.connection import connection
from database.tables._base import DatabaseRecord
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



@connection.register
class GameLogRecord(DatabaseRecord):

    structure = {
        f.team_id      : s.team_id,
        f.game_id      : s.game_id,
        f.team_name    : s.team_name,
        f.team_abbr    : s.team_abbr,
        f.game_date    : s.game_date,
        f.is_home      : s.is_home,
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
    }

    required_fields = [
        f.team_id,
        f.game_id,
        f.team_name,
        f.team_abbr,
        f.game_date,
        f.is_home,
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
    ]

    default_values = {
    }

