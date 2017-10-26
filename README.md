# NBAI - A prediction system for basketball statistics.

Step 1:
	Open up your internet browser.

Step 2:
	Go to the website http://nbai.ddns.net/



## To setup the database:
These instructions assume you're using Ubuntu, preferably 14.04, 15.04, or 16.04.  We also assume you've already installed MongoDB.  Instructions on how to do so can be found on the MongoDB website. You also need python installed on your system (python is typically packaged with Ubuntu so install may not be required).

To set up the server, first run the `preactivate.sh` script

`sudo sh src/preactivate.sh`

This will install all necessary python dependencies so you can host the web server.

Next, to backfill your database, run the backfill.py script.  
`./src/backfill.py`
This will pull stats from every season from 2007 until now.

Once you have this, you're ready to start hosting web traffic.

## Starting server
To start the mongodb server, run `sudo service mongod start`

To start the webserver, run `./src/server.py` and navigate your web browswer to the printed localhost (typically `localhost:5000`). 

The nbAI site is now running locally!
