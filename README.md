# Example Code
The example code in this directory launches a small web app that lets you read/write from a server via a web page.  This demonstrates Flask, pymongo/mongokit, and HTML/CSS all working together.

# Dependencies
I'm assuming both `pip` and `virtualenv` are installed.  **The preactivate script** (which sets up the python environment) **won't work unless those two are installed on your host.**

# To use:
First, run the preactivate.sh script

>    `$ sudo sh preactivate.sh`

This will create a virtual environment from which you can run the server code.

Next, launch the server (from the root directory):

>    `$ ./server.py`

# Endpoints
The server is active at `localhost:5000/`.  The following endpoints are valid:
 * `drop`, `/delete` : Deletes the contents of the database
 * `/show` : Shows the contents of the database
 * `/find` : Searches for a record
 * `/save` : Adds a record to the database
 * All other routes redirect to `/save`

Now, if you go to `localhost:5000/save` and `localhost:5000/find` in your web browser, you can read and write from the database.  You can also delete everything by visiting `localhost:5000/drop` or `localhost:5000/delete`.

Additionally, you can see what records were written to the database from the command line via `read_db.py` and you can delete everything via `delete_db.py`
