#fantasy_points_calculator() function that takes in a players stats for a given game and outputs the calculation of their fantasy points for that given game based on espn's breakdown of points awarded per stat.

def fantasy_point_calc(stats):
	(pts, rb, ast, stl, blk, to) = stats	
	fantasy_points = pts + (rb * 1.2) + (ast * 1.5) + (stl * 3) + (blk * 3 ) + (to * -1)
	return fantasy_points
	
