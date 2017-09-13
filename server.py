#!env/bin/python

import pymongo
from flask import Flask, request, render_template, redirect, url_for
from tables.playerstable import PlayersTable, connection
from tables.basetable import DATABASE_NAME

app = Flask(__name__)

GET = 'GET'
POST = 'POST'



## This redirects all routes other than
## "save" or "find" to the "/save" page
@app.route('/', defaults={'path' : ''})
@app.route('/<path:path>')
def all_unnamed_routes(path):
    return redirect(url_for('save_get'))




@app.route('/save', methods=[GET])
def save_get():
    return render_template('savesave.html')




@app.route('/save', methods=[POST])
def save_post():
    ## Get the stuff from the form on the webpage
    name = request.form['player_name']
    age  = request.form['player_age']

    ## Create a Player object and put these fields into it
    player = connection.PlayersTable()
    player.name = name
    player.age  = age

    ## Save the object to the database
    player.save()

    ## For demonstration purposes only
    return "Saved player {}<br>Objects currently in database:<br>{}".format(player.name, show_db())




@app.route('/find', methods=[GET])
def find_get():
    return render_template('findfind.html')




@app.route('/find', methods=[POST])
def find_post():

    ## Get the name from the text box on the webpage
    name = request.form['player_name']

    ## Create a Player object
    query = {
        PlayersTable.f.name : name
    }

    ## Search for this Player
    result = connection.PlayersTable.find_one(query)

    ## If this player does not exist, tell the user
    if result is None:
        return "{} doesn't exist".format(request.form['player_name'])

    ## Otherwise, print the player's info
    player = result[0]
    return "Name : {}<br>Age : {}".format(player.name, player.age)




@app.route('/drop')
@app.route('/delete')
def delete_everything():
    pymongo.Connection().drop_database(DATABASE_NAME)
    return "Deleted everything (including this database)"

@app.route('/show')
def show_everything():
    return show_db()


## For demonstration porpoises only.
## Don't focus too much on what's happening here.
## IT's ugly af and only used to print database contents
def show_db():
    from tables.playerstable import TABLE_NAME
    from tables.basetable import DATABASE_NAME
    table = getattr(pymongo.Connection(), DATABASE_NAME)[TABLE_NAME].find()
    elems = ['{} records found'.format(table.count())]
    for record in table:
        elems.append("===========================================================")
        for k in record.keys():
            elems.append("{} : {}".format(k, record[k]))
    return '<br>'.join((elems))



if __name__ == '__main__':
    app.run(debug=True, port=5000)

