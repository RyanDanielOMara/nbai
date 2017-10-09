import datetime
from mongokit import Document
from database.connection import connection, DATABASE_NAME
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



def current_utctime():
    return unicode(datetime.datetime.utcnow())

@connection.register
class DatabaseRecord(Document):

    __database__ = DATABASE_NAME

    structure = {
        f.date_created : s.date_created,
        f.date_updated : s.date_updated,
    }

    required_fields = [
        f.date_created,
        f.date_updated,
    ]

    default_values = {
        f.date_created : current_utctime,
        f.date_updated : current_utctime,
    }

    ## Updates the 'date_updated' timestamp
    def save(self):
        self[f.date_updated] = current_utctime()
        super(DatabaseRecord, self).save()
        return

    ## Allows you to get fields directly,
    ## ex: Player.name instead of Player["name"]
    def __getattr__(self, field):
        if field in self.keys():
            return self[field]
        return Document.__getattr__(self, field)

    ## Allows you to set fields directly
    def __setattr__(self, field, value):
        if field in self.keys():
            #if isinstance(value, basestring):
            #    value = unicode(value)
            self[field] = value
        Document.__setattr__(self, field, value)

