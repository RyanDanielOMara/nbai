#!env/bin/python
import argparse
import flask

app = flask.Flask(__name__)

some_list = ['Name', 'Team', 'Position', 'Opponent', 'Our Predictions']


value_column_index = 4;
position_column_index = 2;
team_column_index= 1;
name_column_index =0;

nbai = [
 ['LeBron James', 'CLE', 'SF', 'BOS', 28],
 ['Kevin Durant', 'GSW', 'SF', 'HOU', 26],
 ['Kevin Love', 'CLE', 'C', 'BOS', 22],
 ['Stephen Curry', 'GSW', 'PG', 'HOU', 22],
 ['James Harden', 'HOU', 'SG', 'GSW', 21],
 ['Al Horford', 'BOS', 'SF', 'CLE', 21],
 ['David West', 'GSW', 'PF', 'HOU', 19],
 ['Deron Williams', 'CLE', 'PG', 'BOS', 19],
 ['Kyrie Irving', 'BOS', 'PG', 'CLE', 18],
 ['Andre Iguodala', 'GSW', 'SF', 'HOU', 17],
 ['Isaiah Thomas', 'CLE', 'PG', 'BOS', 15],
 ['Klay Thompson', 'GSW', 'SG', 'HOU', 14],
 ['Eric Gordon', 'HOU', 'PF', 'GSW', 14],
 ['Trevor Ariza', 'HOU', 'PF', 'GSW', 14],
 ['Tristan Thompson', 'CLE', 'PF', 'BOS', 13],
 ['Ryan Anderson', 'HOU', 'PF', 'GSW', 13],
 ['Lou Williams', 'HOU', 'SG', 'GSW', 12],
 ['Amir Johnson', 'BOS', 'SF', 'CLE', 12],
 ['Matt Barnes', 'GSW', 'PG', 'HOU', 11],
 ['Tyler Zeller', 'BOS', 'PG', 'CLE', 11],
 ['Draymond Green', 'GSW', 'C', 'HOU', 11],
 ['JaVale McGee', 'GSW', 'C', 'HOU', 11],
 ['JR Smith', 'CLE', 'SG', 'BOS', 11],
 ['Patrick Beverley', 'HOU', 'PF', 'GSW', 11],
 ['Richard Jefferson', 'CLE', 'PF', 'BOS', 11],
 ['Kelly Olynyk', 'BOS', 'SG', 'CLE', 11],
 ['Channing Frye', 'CLE', 'SF', 'BOS', 10],
 ['Marcus Smart', 'BOS', 'PF', 'CLE', 10],
 ['Kyle Korver', 'CLE', 'SG', 'BOS', 10],
 ['Derrick Williams', 'CLE', 'PG', 'BOS', 9],
 ['Zaza Pachulia', 'GSW', 'PF', 'HOU', 9],
 ['Jonas Jerebko', 'BOS', 'C', 'CLE', 9],
 ['Shaun Livingston', 'GSW', 'DF', 'HOU', 8]
]


teamlist = ['CLE', 'GSW', 'HOU', 'BOS']


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
        value_index=value_column_index,
        team_list = teamlist
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000, type=int, choices=xrange(1, 65536))
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
        app.run(host=args.host, port=args.port)

