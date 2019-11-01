#!env/bin/python
import datetime
import os
import time

date_updated = datetime.date.today()

def do_server_update():
    os.popen("killall server.py").read()
    os.popen('./src/server.py').read()

def do_git_pull():
    os.chdir("/var/www/nbai_live")
    result = os.popen("git pull").read()

    if result != 'Already up-to-date.\n':
        do_server_update()
        
while True:
    if datetime.date.today() > date_updated and datetime.datetime.now().hour >= 3:
        do_server_update()
        date_updated = datetime.date.today()

    do_git_pull()
    time.sleep(20)

