#!env/bin/python
import flask
import sys

app = flask.Flask(__name__)

some_list = ['Name', 'Team', 'Position', 'ESPN Score', 'Our Predictions']

some_dict = {
    'LeBron Jamz' : ['CLE', 23, 61],
    'Kobe Bryant' : ['LAL', 8,  81]
}

value_column_index = 4;
position_column_index = 2;
team_column_index= 1;
name_column_index =0;

nbai = [
['LeBron James', 'CLE', 'SF', '30', 'UnderValued'],
['Isaiah Thomas', 'CLE', 'PG', '25', 'OverValued'],
['Steph Curry', 'GSW', 'PG', '25', 'UnderValued']
]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home_page(path):
    return flask.render_template(
    	'index.html',
    	header_list=some_list,
        website_table=nbai,
        position_index=position_column_index,
        team_index=team_column_index,
        name_index=name_column_index,
        value_index=value_column_index
    	)

if len(sys.argv) != 2:
    print("Please add a server port as a command line argument.")
    exit()
else:
    try:
        int(sys.argv[1])
    except ValueError:
	print("Command line argument invalid! \n Argument should be the listening port of the server. \n (Integer between 1 and 65535)")
	exit()
	
    if  (sys.argv[1] > 1 and sys.argv[1] < 65535): 
	print("Command line argument incorrect! \n Argument should be the listening port of the server. \n (Integer between 1 and 65535) ")
        exit()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=sys.argv[1])

