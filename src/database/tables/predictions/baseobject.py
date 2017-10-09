from mongokit import Document, Connection
import datetime


DATABASE_NAME = 'NBAI'
connection = Connection()


def current_utctime():
	return unicode(datetime.datetime.utcnow())


@connection.register
class BaseObject(Document):

    __database__ = DATABASE_NAME

    class e:
        date_created = 'date_created'
        date_updated = 'date_updated'

    structure = {
        e.date_created : unicode,
        e.date_updated : unicode,
    }

    required_fields = [
        e.date_created,
        e.date_updated,
    ]

    default_values = {
        e.date_created : current_utctime,
        e.date_updated : current_utctime,
    }

    ## Updates the 'date_updated' timestamp
    def save(self):
        self[self.e.date_updated] = current_utctime()
        super(BaseObject, self).save()
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
            if isinstance(value, basestring):
                value = unicode(value)
            self[field] = value
        Document.__setattr__(self, field, value)
