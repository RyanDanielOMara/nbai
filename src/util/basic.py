import logging



def get_gid_tid(nba_data):
    return (nba_data['GAME_ID'], nba_data['TEAM_ID'])



def identity(nba_data, nba_key):
    return nba_data.get(nba_key, None)


"""
Sort issue was sorting ints as strings.
"""
def cast_int(nba_data, nba_key):
    try:
        return int(nba_data[nba_key])
    except:
        msg = 'Cannot convert "{}" to int.  Returning 0.'
        datum = nba_data[nba_key]
        logging.warning(msg.format(datum))
    return 0



def is_home(nba_data, nba_key):
    try:
        return nba_data['MATCHUP'][:3] == nba_data['TEAM_ABBREVIATION']
    except:
        msg = 'Cannot determine who is home.\n  (GAME_ID : {}) (TEAM_ID : {})'
        game_id, team_id = get_gid_tid(nba_data)
        logging.warning(msg.format(game_id, team_id))
    return False



def is_win(nba_data, nba_key):
    try:
        return nba_data[nba_key].strip()[0] == 'W'
    except:
        msg = 'Cannot determine who won.\n  (GAME_ID : {}) (TEAM_ID : {})'
        game_id, team_id = get_gid_tid(nba_data)
        logging.warning(msg.format(game_id, team_id))
    return False



def get_player_game_id(nba_data, nba_key):
    return  str(int(nba_data['PLAYER_ID'])) + nba_data['GAME_ID']



def get_team_game_id(nba_data, nba_key):
    return  str(int(nba_data['TEAM_ID'])) + nba_data['GAME_ID']



def get_season(year):
    return '{}-{}'.format(year, str(year+1)[2:])



def get_height(nba_data, nba_key):
    try:
        f, i = nba_data[nba_key].split('-')
        return 12 * int(f) + int(i)
    except:
        msg = 'Error converting height to inches: {}'
        logging.warning(msg.format(nba_data[nba_key]))
        return None



def get_dob(nba_data, nba_key):
    try:
        return nba_data[nba_key][:10]
    except:
        msg = 'Error parsing dob: {}'
        logging.warning(msg.format(nba_data[nba_key]))
        return None



"""
Decorator for logging the call stack.
Prints the name of the function, as well as the params
"""
def log_call_stack(func):
    def anon(*args, **kwargs):
        quoted = lambda v : '"{}"'.format(v) if isinstance(v, basestring) else v
        fargs = ', '.join([str(arg) for arg in args])
        fkwargs = ', '.join(['{}={}'.format(k, quoted(v)) for k, v in kwargs.items()])
        if len(fargs) > 0 and len(fkwargs) > 0:
            params = '{}, {}'.format(fargs, fkwargs)
        elif len(fargs) > 0:
            params = fargs
        else:
            params = fkwargs
        fcall = '{}({})'.format(func.__name__, params)
        logging.debug('FUNCTION CALL: {}'.format(fcall))
        val = func(*args, **kwargs)
        logging.debug('FUNCTION RTRN: {}'.format(fcall))
        return val
    return anon

