from baseobject import BaseObject, connection

TABLE_NAME = 'team_group_tally'

@connection.register
class TeamGroupTallyObject(BaseObject):

	__collection__ = TABLE_NAME


    ## This class only exists to prevent typos.
    ## It's not needed, but it adds a layer of safety.
	class f():
		team_id = 'team_id'
		fantasy_pts_a  = 'fantasy_pts_a'
		fantasy_min = 'fantasy_min'
	

	'''	
	small_players_pts = 'small_players_pts' 			
	small_players_min = 'small_players_min'			
	large_players_pts = 'large_players_pts'
	large_players_min = 'large_players_min'
	'''		

	structure = {
		f.team_id : int,
		f.fantasy_pts_a : int,
		f.fantasy_min : int

	}
	'''       
	f.small_players_pts : unicode,
	f.small_players_min : unicode,
	f.large_players_pts : unicode,
	f.large_players_min : unicode		
	'''
	

	required_fields = [
		f.team_id,
		f.fantasy_pts_a,
		f.fantasy_min
	]
	'''
    f.small_players_pts,
	f.small_players_min,
	f.large_players_pts,
	f.large_players_min	
	'''	

    

	default_values = {
		f.fantasy_pts_a : 0,
		f.fantasy_min : 0
    }
