from predictioncalc import *
from baseobject import connection
from playertallyobject import *
from teamgrouptallyobject import *
from fantasycalc import *
from predictionobject import *
from percentdiff import *
import csv

#BACKTEST

with open('Player_Boxscores.csv','r') as f:
	things_to_save = {}
	players_found = {}
	f.readline()
	skip_count = 0	
	key = 0
	for line in f:
		line = line.split(',')
		players_found[line[7]] = 1
		skip_count += 1
		if skip_count == 200000:
			break
	
	i = 0
	for row in f:
		i += 1
		if i % 1000 == 0:
			print("things to save run: " + str(i))
		
		if i == 65000:
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
		
		if person_id in players_found:
				
			key += 1
				
		
			if key not in things_to_save:
				
				things_to_save[key] = connection.PredictionObject()
				things_to_save[key].player_id = int(person_id)
									
				p_fantasy_pts = prediction_calc(int(person_id),int(vs_team_id))
				a_fantasy_pts = fantasy_point_calc(pts,blk_shots,stl,ast,rb,fgm,fga,ft,fta,to)	
				percent_diff_r = percent_diff(p_fantasy_pts,a_fantasy_pts)
		
				things_to_save[key].team_id = int(vs_team_id)
				things_to_save[key].game_id = int(game_id)	
				things_to_save[key].date = date
				things_to_save[key].predicted_pts = p_fantasy_pts
				things_to_save[key].actual_pts = a_fantasy_pts
				things_to_save[key].percent_diff = percent_diff_r
			
		
			
			
			

	print(str(len(players_found)))	
	print(str(len(things_to_save)))
	
	y = 0	
	for k,v in things_to_save.items():
		y += 1
		print("saving to database: " + str(y))	
		v.save()
		

