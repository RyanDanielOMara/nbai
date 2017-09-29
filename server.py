#!env/bin/python
import flask
app = flask.Flask(__name__)

some_list = ['Name', 'Team', 'Position', 'ESPN Score', 'Our Predictions']

some_dict = {
    'LeBron Jamz' : ['CLE', 23, 61],
    'Kobe Bryant' : ['LAL', 8,  81]
}

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
        website_table=nbai
    	)


if __name__ == '__main__':
    app.run(port=5000)
