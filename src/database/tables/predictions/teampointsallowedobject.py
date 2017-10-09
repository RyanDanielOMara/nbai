from baseobject import BaseObject, connection

TABLE_NAME = 'team_group_tally'

@connection.register
class PlayerTallyObject(BaseObject):

    __collection__ = TABLE_NAME


    ## This class only exists to prevent typos.
    ## It's not needed, but it adds a layer of safety.
    class f():
	player_id = 'player_id'
	sum_of_fantasy_pts = 'sum_of_fantasy_pts' 			
	sum_of_min_played = 'sum_of_min_played'			
		
		

    structure = {
	f.player_id : unicode,
       	f.sum_of_fantasy_pts : unicode,
	f.sum_of_min_played : unicode		
	}

    required_fields = [
        f.player_id,
        f.sum_of_fantasy_pts,
	f.sum_of_min_played,
	

    ]

    default_values = {
	#no default values
    }
