#!../env/bin/python
import argparse
import flask

app = flask.Flask(__name__)

some_list = ['Name', 'Team', 'Position', 'Opponent', 'Our Predictions', 'Value']


value_column_index = 5;
position_column_index = 2;
team_column_index= 1;
name_column_index =0;

nbai = [
    ['LeBron James', 'CLE', 'SF', 'BOS', 28, 'Overvalued'],
    ['Kevin Durant', 'GSW', 'SF', 'HOU', 26, 'Overvalued'],
    ['Kevin Love', 'CLE', 'C', 'BOS', 22, 'Overvalued'],
    ['Stephen Curry', 'GSW', 'PG', 'HOU', 22, 'Undervalued'],
    ['James Harden', 'HOU', 'SG', 'GSW', 21, 'Undervalued'],
    ['Al Horford', 'BOS', 'SF', 'CLE', 21, 'Overvalued'],
    ['David West', 'GSW', 'PF', 'HOU', 19, 'Overvalued'],
    ['Deron Williams', 'CLE', 'PG', 'BOS', 19, 'Overvalued'],
    ['Kyrie Irving', 'BOS', 'PG', 'CLE', 18, 'Undervalued'],
    ['Andre Iguodala', 'GSW', 'SF', 'HOU', 17, 'Undervalued'],
    ['Isaiah Thomas', 'CLE', 'PG', 'BOS', 15, 'Undervalued'],
    ['Klay Thompson', 'GSW', 'SG', 'HOU', 14, 'Undervalued'],
    ['Eric Gordon', 'HOU', 'PF', 'GSW', 14, 'Overvalued'],
    ['Trevor Ariza', 'HOU', 'PF', 'GSW', 14, 'Overvalued'],
    ['Tristan Thompson', 'CLE', 'PF', 'BOS', 13, 'Undervalued'],
    ['Ryan Anderson', 'HOU', 'PF', 'GSW', 13, 'Overvalued'],
    ['Lou Williams', 'HOU', 'SG', 'GSW', 12, 'Overvalued'],
    ['Amir Johnson', 'BOS', 'SF', 'CLE', 12, 'Undervalued'],
    ['Matt Barnes', 'GSW', 'PG', 'HOU', 11, 'Undervalued'],
    ['Tyler Zeller', 'BOS', 'PG', 'CLE', 11, 'Overvalued'],
    ['Draymond Green', 'GSW', 'C', 'HOU', 11, 'Overvalued'],
    ['JaVale McGee', 'GSW', 'C', 'HOU', 11, 'Overvalued'],
    ['JR Smith', 'CLE', 'SG', 'BOS', 11, 'Undervalued'],
    ['Patrick Beverley', 'HOU', 'PF', 'GSW', 11, 'Undervalued'],
    ['Richard Jefferson', 'CLE', 'PF', 'BOS', 11, 'Overvalued'],
    ['Kelly Olynyk', 'BOS', 'SG', 'CLE', 11, 'Undervalued'],
    ['Channing Frye', 'CLE', 'SF', 'BOS', 10, 'Overvalued'],
    ['Marcus Smart', 'BOS', 'PF', 'CLE', 10, 'Undervalued'],
    ['Kyle Korver', 'CLE', 'SG', 'BOS', 10, 'Overvalued'],
]
#    ['Derrick Williams', 'CLE', 'PG', 'BOS', 9, 'Overvalued'],
#    ['Zaza Pachulia', 'GSW', 'PF', 'HOU', 9, 'Overvalued'],
#    ['Jonas Jerebko', 'BOS', 'C', 'CLE', 9, 'Overvalued'],
#    ['Shaun Livingston', 'GSW', 'DF', 'HOU', 8, 'Overvalued']


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

