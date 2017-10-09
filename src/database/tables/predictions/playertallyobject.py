from baseobject import BaseObject, connection
#name of table in database
TABLE_NAME = 'player_tally'

@connection.register
class PlayerTallyObject(BaseObject):

	__collection__ = TABLE_NAME


    ## This class only exists to prevent typos.
    ## It's not needed, but it adds a layer of safety.
	class f():
		player_id = 'player_id'
		sum_of_fantasy_pts = 'sum_of_fantasy_pts' 			
		sum_of_min_played = 'sum_of_min_played'
		games_played = 'games_played'			
		
		

	structure = {
		f.player_id : int,
		f.sum_of_fantasy_pts : int,
		f.sum_of_min_played : int,
		f.games_played : int		
	}

	required_fields = [
		f.player_id,
		f.sum_of_fantasy_pts,
		f.sum_of_min_played,
		f.games_played
	

    ]

	default_values = {
		f.sum_of_fantasy_pts : 0,
		f.sum_of_min_played : 0,
		f.games_played : 0,
    }

