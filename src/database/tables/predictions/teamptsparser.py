from teamptsavg import *
from teamgrouptallyobject import *

bp = connection.TeamPtsAvgObject()


for team in connection.TeamGroupTallyObject.find():
	bp.points_a += team.fantasy_pts_a
	bp.min_a += team.fantasy_min
	
bp.save()
	
	
	
