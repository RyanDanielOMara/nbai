"""
The purpose of this class is to store data from stats.nba.com in a
more uniform format.  The site returns JSON nodes, each of which has
a wide variety of keys that differ from the keys used in our database.
Additionally, their keys will change depending on the endpoint that the
response comes from (ex: sometimes PLAYER_ID gets replaced with PERSON_ID).

To remedy this, this class serves as a container that parses out all relevant
info from these JSON nodes and stores it internally (using the fields we use).

Any class that inherits from this needs to set these fields:


    self.attrs : A dict containing <our_field : nba_key> pairs.
                 These are the fields that will be present in our
                 object (ex: node.player_id, node.dob, etc).  If there
                 is no corresponding nba_key, use None (or whatever).

    example:
    self.attrs = {
        'player_id'   : 'PERSON_ID',
        'player_name' : 'FIRST_NAME_LAST_NAME'
    }



    self.parsers : A dict containing <attr_field : parsing_function> pairs.
                   These functions are responsible for parsing the value in nba_dict
                   (ex: casting 'PLAYER_ID' to an int, or converting 'HEIGHT' to inches).
                   All functions must take two arguments (typically nba_dict, nba_key).
                   Any undefined parsers will return the raw value in nba_dict[nba_key].
    example:
    self.parsers = {
        'player_id' : cast_as_int
    }


"""
class BaseNode:
    def __init__(self, nba_data):
        raise NotImplementedError("This class is meant to be inherited.")

    def init_attrs(self, nba_data):
        self.json = nba_data
        for attr, nba_key in self.attrs.items():
            setattr(self, attr, self.parsers.get(attr, self._identity)(nba_data, nba_key))
        return

    def _identity(self, nba_data, nba_key):
        return nba_data.get(nba_key, None)

