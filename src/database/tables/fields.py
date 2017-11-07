"""
Fields contains all of the fields used in the database object.

By centralizing this into one class, we can ensure that no typos
occur throughout our code (because runtime errors will occur if
we try to access a nonexistient field, such as 'plyaer_id')
"""
class Fields:
    ast            = 'ast'
    blk            = 'blk'
    color          = 'color'
    colors         = 'colors'
    conference     = 'conference'
    country        = 'country'
    date_created   = 'date_created'
    date_updated   = 'date_updated'
    division       = 'division'
    dob            = 'dob'
    draft_overall  = 'draft_overall'
    draft_round    = 'draft_round'
    draft_year     = 'draft_year'
    dreb           = 'dreb'
    exp            = 'exp'
    fg3a           = 'fg3a'
    fg3m           = 'fg3m'
    fga            = 'fga'
    fgm            = 'fgm'
    first_year     = 'first_year'
    fouls          = 'fouls'
    fta            = 'fta'
    ftm            = 'ftm'
    game_date      = 'game_date'
    game_id        = 'game_id'
    game_log_saved = 'game_log_saved'
    games_dict     = 'games_dict'
    games_played   = 'games_played'
    has_bio        = 'has_bio'
    height         = 'height'
    is_home        = 'is_home'
    jersey         = 'jersey'
    last_year      = 'last_year'
    minutes        = 'minutes'
    oreb           = 'oreb'
    player_game_id = 'player_game_id'
    player_id      = 'player_id'
    player_name    = 'player_name'
    plus_minus     = 'plus_minus'
    position       = 'position'
    pre_nba        = 'pre_nba'
    pts            = 'pts'
    reb            = 'reb'
    roster         = 'roster'
    season         = 'season'
    stl            = 'stl'
    team_abbr      = 'team_abbr'
    team_game_id   = 'team_game_id'
    team_id        = 'team_id'
    team_name      = 'team_name'
    tov            = 'tov'
    weight         = 'weight'
    won            = 'won'
    def __init__(self):
        raise NotImplementedError("Don't instantiate me!")



"""
Structure contains all of the types for the various fields of the database.

By centralizing this into one place, we can ensure any DatabaseRecord that uses
a particular field has the same data type.  This prevents mismatching key errors,
like if a PlayerRecord represents player_id with an int but PlayerGameLogRecord
uses a basestring.
"""
class Structure:
    ast            = int
    blk            = int
    color          = basestring
    colors         = [basestring]
    conference     = basestring
    country        = basestring
    date_created   = basestring
    date_updated   = basestring
    division       = basestring
    dob            = basestring
    draft_overall  = basestring
    draft_round    = basestring
    draft_year     = basestring
    dreb           = int
    exp            = int
    fg3a           = int
    fg3m           = int
    fga            = int
    fgm            = int
    first_year     = int
    fouls          = int
    fta            = int
    ftm            = int
    game_date      = basestring
    game_id        = basestring
    game_log_saved = bool
    games_dict     = { basestring : [basestring] }
    games_played   = int
    has_bio        = bool
    height         = int
    is_home        = bool
    jersey         = basestring
    last_year      = int
    minutes        = int
    oreb           = int
    player_game_id = basestring
    player_id      = int
    player_name    = basestring
    plus_minus     = int
    position       = basestring
    pre_nba        = basestring
    pts            = int
    reb            = int
    roster         = [int]
    season         = int
    stl            = int
    team_abbr      = basestring
    team_game_id   = basestring
    team_id        = int
    team_name      = basestring
    tov            = int
    weight         = int
    won            = bool
    def __init__(self):
        raise NotImplementedError("Don't instantiate me!")

