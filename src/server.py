#!env/bin/python
import argparse
import flask
import pymongo

from database.connection import DATABASE_NAME, connection
from datetime import date
from util.players_util import extract_player_info, load_todays_players, get_todays_games


app = flask.Flask(__name__)

some_list = ['Name', 'Team', 'Position', 'Opponent', 'Our Predictions', 'Value']
teamlist = get_todays_games()

name_column_index     = 0;
position_column_index = 2;
team_column_index     = 1;
value_column_index    = 5;

todays_players = load_todays_players()

@app.route('/', defaults={'path': ''})
@app.route('/index.html', defaults={'path': '/index.html'})
def home_page(path):



    return flask.render_template(
        'index.html',
        header_list    = some_list,
        website_table  = todays_players,
        position_index = position_column_index,
        team_index     = team_column_index,
        name_index     = name_column_index,
        value_index    = value_column_index,
        team_list      = teamlist
    )


@app.route('/players/<playerid>')
def player_page(playerid):
    player = extract_player_info(playerid)
    if(player):
        return flask.render_template(
            'players_page.html',
            player = player
        )
    else:
        return flask.abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000, type=int, choices=xrange(1, 65536))
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    app.run(host=args.host, port=args.port)
