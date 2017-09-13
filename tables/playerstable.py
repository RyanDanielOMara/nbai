from basetable import BaseTable, connection

TABLE_NAME = 'players'

@connection.register
class PlayersTable(BaseTable):

    __collection__ = TABLE_NAME


    ## This class only exists to prevent typos.
    ## It's not needed, but it adds a layer of safety.
    class f():
        name = 'name'
        age  = 'age'

    structure = {
        f.name : unicode,
        f.age  : unicode,
    }

    required_fields = [
        f.name,
        f.age,
    ]

    default_values = {
    }

