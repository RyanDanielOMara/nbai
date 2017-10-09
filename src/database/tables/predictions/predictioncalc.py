from random import *
from playertallyobject import *
from teamgrouptallyobject import *
from teamptsavg import *
'''
f(x,Y) = R(x,Y) + [1 + PC(Y,p(x))] * PS(x)

The following can be defined as:
x = player in question
Y = team player is playing against
R(x,Y) = random factor (Will be using a RNG for now, can be changed to a different factor in future)
PC(Y,p(x)) = percent boost team Y gives, for the current p(x) (group of player x)
PS(x) = expected points a player will score based on avg points per min * min expected to play
'''


def prediction_calc(player_id,team_id):
	prediction = 0	
	rand_factor = uniform(0,1)
	
	query = connection.TeamGroupTallyObject.find({'team_id' : team_id})	
	check_query = connection.TeamGroupTallyObject.find({'team_id' : team_id}).count()
	 
	if check_query == 0:
		print("FUCKED UP FINDING UP TEAM ID: " + str(team_id))
		
	
	
	teams_avg_pts_min = 1.0 * query[0]['fantasy_pts_a'] / query[0]['fantasy_min']
	
	query1 = connection.TeamPtsAvgObject.find()[0]
	check_query1 = connection.TeamPtsAvgObject.find()[0]
	
	if check_query1 == 0:
		print("FUCKED UP FINDING LEAGUE STATS")
				
	 
 
	league_avg_pts_min = 1.0 * query1['points_a'] / query1['min_a']
 
	boost = ((teams_avg_pts_min - league_avg_pts_min)/league_avg_pts_min)
	
	query2 = connection.PlayerTallyObject.find({'player_id' : player_id})
	check_query2 = connection.PlayerTallyObject.find({'player_id' : player_id}).count()
	
	
	if check_query2 == 0:	
		print("FUCKED UP FINDING PLAYER ID: " + str(player_id))
		
	

	player_avg_pts_min = 1.0 * query2[0]['sum_of_fantasy_pts'] / query2[0]['sum_of_min_played']
	
	player_expected_min = 1.0 * query2[0]['sum_of_min_played'] / query2[0]['games_played']
	expected_points = player_avg_pts_min * player_expected_min  
	prediction = rand_factor + (1 + boost) * expected_points
	return prediction
