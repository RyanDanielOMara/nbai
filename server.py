#!env/bin/python
import flask
app = flask.Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home_page(path):
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000)
