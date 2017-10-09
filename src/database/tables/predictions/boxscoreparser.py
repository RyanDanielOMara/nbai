from baseobject import connection
from playertallyobject import *
from teamgrouptallyobject import *
from fantasycalc import *
import csv
#GOD

with open('Player_Boxscores.csv','r') as f:
	things_to_save = {}
	f.readline()
	i = 0
	for row in f:
		i += 1
		if i % 1000 == 0:
			print("things to save run: " + str(i))
		
		if i == 200000:
			break		
		
		row = row.split(',')
		game_id = row[0]
		season = row[1]
		season_type = row[2]
		game_no = row[3]
		playoff_rd = row[4]
		playoff_rd_game_no = row[5]
		date = row[6]
		person_id = row[7]
		player_name = row[8]
		team_id = row[9]
		abbrev = row[10]
		location = row[11] 
		outcome = row[12]
		vs_team_id = row[13]
		min_played = row[14]
		sec_played = row[15]
		pts = int(row[16])
		rb = int(row[17])
		ast = int(row[18])
		stl = int(row[19])
		to = int(row[20])
		blk_shots = int(row[21])
		personal_fouls = row[22]
		fgm = int(row[23])
		fga = int(row[24])
		three_pts_m = row[25]
		three_pts_a =row[26]
		ft = int(row[27])
		fta = int(row[28])
		off_rb = row[29]
		def_rb = row[30]
		tech_fouls = row[31]
		flag_fouls = row[32]
		ejections = row[33]
		points_in_paint = row[34] 
		fast_break_pts = row[35]
		triple_doubles = row[36]
		double_doubles = row[37]
		plus_minus = row[38]
		blk_against = row[39]
		pts_off_to = row[40]
		second_chance_pts = row[41]


		if person_id not in things_to_save:
			things_to_save[person_id] = connection.PlayerTallyObject()
			things_to_save[person_id].player_id = int(person_id)

        
		fantasy_pts = fantasy_point_calc(pts,blk_shots,stl,ast,rb,fgm,fga,ft,fta,to)	

		things_to_save[person_id].sum_of_fantasy_pts += fantasy_pts
		things_to_save[person_id].games_played +=  1	
		things_to_save[person_id].sum_of_min_played +=  int(min_played)
		

		
		if vs_team_id not in things_to_save:
			things_to_save[vs_team_id] = connection.TeamGroupTallyObject()
			things_to_save[vs_team_id].team_id = int(vs_team_id)	


		things_to_save[vs_team_id].fantasy_pts_a += fantasy_pts
		things_to_save[vs_team_id].fantasy_min += int(min_played)
	y = 0	
	for k,v in things_to_save.items():
		y += 1
		print("saving to database: " + str(y))	
		v.save()
		
