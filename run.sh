#!/bin/bash

PRIMARY_BLOG='travelsmart' 
EXTRA_BLOGS=('bozho' 'az_moga' 'igicheva' 'pateshestvenik')

clean_up () {
    echo Terminating...
    pkill flask
    exit
}

trap clean_up SIGINT SIGTERM

# Scrape some initial data
echo Sraping $PRIMARY_BLOG...
python3 main.py $PRIMARY_BLOG

# Start up the server and open the home page
echo Starting server...
export FLASK_APP=web_instance.py
flask run >/dev/null 2>/dev/null &
sleep 1
xdg-open http://127.0.0.1:5000/

# Scrape the other blogs
for SINGLE_BLOG in ${EXTRA_BLOGS[@]}
do
    echo Sraping $SINGLE_BLOG...
    python3 main.py $SINGLE_BLOG
done

# Wait for the user to be done browsing
echo "Press return to terminate server"
read

clean_up
