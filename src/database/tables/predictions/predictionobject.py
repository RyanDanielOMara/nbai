from baseobject import BaseObject, connection

TABLE_NAME = 'predictions'

@connection.register
class PredictionObject(BaseObject):

	__collection__ = TABLE_NAME


    ## This class only exists to prevent typos.
    ## It's not needed, but it adds a layer of safety.
	class f():
		player_id = 'player_id'
		team_id = 'team_id'
		game_id = 'game_id'
		date = 'date'
		predicted_pts = 'predicted_pts'
		actual_pts = 'actual_pts'
		percent_diff = 'percent_diff'

	structure = {
		f.player_id : int,
		f.game_id : int,
        f.team_id : int,
        f.date : unicode,
        f.predicted_pts : float,
        f.actual_pts : int,
        f.percent_diff : float
	}

	required_fields = [
		f.player_id,
		f.game_id,
		f.team_id,
        f.date,
        f.predicted_pts,
        f.actual_pts,
        f.percent_diff
		
    ]

	default_values = {
	#no default values
    }
