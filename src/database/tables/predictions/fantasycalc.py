#fantasy_points_calculator() function that takes in a players stats for a given game and outputs the calculation of their fantasy points for that given game based on espn's breakdown of points awarded per stat.

def fantasy_point_calc(pts,blk,stl,ast,rb,fgm,fga,ft,fta,to):
	fantasy_points = pts + blk + stl + ast + rb+ fgm + (-1 * fga) + ft + (-1 *fta) + (-1 * to)
	return fantasy_points
	
