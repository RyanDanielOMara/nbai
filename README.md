NBAI - A prediction system for basketball statistics.

Step 1:
	Open up your internet browser.

Step 2:
	Go to the website http://nbai.ddns.net/



## To setup the database:
These instructions assume you're using Ubuntu, preferably 14.04, 15.04, or 16.04.  We also assume you've already installed MongoDB.  Instructions on how to do so can be found on the MongoDB website.

To set up the server, first run the `preactivate.sh` script

sudo sh preactivate.sh

This will install all necessary python dependencies so you can host the web server.

Next, to backfill your database, run the backfill.py script.  This will pull stats from every season from 2007 until now.

Once you have this, you're ready to start hosting web traffic.
