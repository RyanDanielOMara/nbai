#!env/bin/python
import flask
app = flask.Flask(__name__)


some_list = [ 'Name', 'Team', 'Number', 'Most points in a game' ]

some_dict = {
    'LeBron Jamz' : ['CLE', 23, 61],
    'Kobe Bryant' : ['LAL', 8,  81]
}

@app.route('/', defaults={'path' : ''})
@app.route('/<path:path>')
def all_unnamed_routes(path):
    return flask.render_template(
            'example.html',
            player_dict=some_dict,
            header_list=some_list
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
