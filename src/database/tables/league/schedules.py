from database.connection import connection
from database.tables._base import DatabaseRecord
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



TABLE_NAME = 'schedules'

@connection.register
class ScheduleRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.game_date      : s.game_date,
        f.game_id        : s.game_id,
        f.team_id        : s.team_id,
        f.is_home        : s.is_home,
        f.game_log_saved : s.game_log_saved,
    }

    indexes = [
        {
            'fields' : [f.game_date],
            'unique' : False
        }
    ]

    required_fields = [
        f.game_date,
        f.game_id,
        f.team_id,
        f.is_home,
        f.game_log_saved,
    ]

    default_values = {
        f.game_log_saved : False,
    }

