#!env/bin/python
import flask
app = flask.Flask(__name__)


some_list = [ 'Name', 'Team', 'Number', 'Most points in a game' ]

some_dict = {
    'LeBron Jamz' : ['CLE', 23, 61],
    'Kobe Bryant' : ['LAL', 8,  81]
}

nbai = [
['First Name', 'Last Name', 'Team', 'Position', 'ESPN Score', 'Our Predictions'],
['LeBron', 'James', 'CLE', 'SF', '30', 'UnderValued'],
['Isaiah', 'Thomas', 'CLE', 'PG', '25', 'OverValued']
]

@app.route('/', defaults={'path' : ''})
@app.route('/<path:path>')
def all_unnamed_routes(path):
    return flask.render_template(
            'index.html',
            
            website_table=nbai
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
