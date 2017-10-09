from predictionobject import *

avg_percent_chg = 0
sum_percent_chg = 0
entries = 0
for row in connection.PredictionObject.find({'player_id' : 2544}):
	sum_percent_chg += row['percent_diff']
	entries += 1

avg_percent_chg = sum_percent_chg / entries

print("The average percent difference between our prediction and actual fantasy points scored is: " + str(avg_percent_chg))  

