from baseobject import BaseObject, connection

TABLE_NAME = 'team_avg_pts_a'

@connection.register
class TeamPtsAvgObject(BaseObject):

	__collection__ = TABLE_NAME
	## This class only exists to prevent typos.
	## It's not needed, but it adds a layer of safety.
	class f():
		points_a = 'points_a'	
		min_a = 'min_a' 			
      	
		

	structure = {
		f.points_a : int,
		f.min_a : int,
      
	
		}

	required_fields = [
		f.points_a,
		f.min_a

    ]

	default_values = {
		f.points_a : 0,
		f.min_a : 0
    }


