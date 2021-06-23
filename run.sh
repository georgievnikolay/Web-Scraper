#!/bin/bash

PRIMARY_BLOG='travelsmart' 
EXTRA_BLOGS=('bozho' 'az_moga' 'igicheva' 'pateshestvenik')

# Make sure to terminate the server, even if we exit forcefully
clean_up () {
    echo Terminating...
    pkill flask
    exit
}

trap clean_up SIGINT SIGTERM

# Check for a valid argument - number of posts to scrape
if [[ $1 ]]
then
    if [[ $1 =~ ^[0-9]+$ ]]
    then
        NUM_POSTS=$1
    else
        echo Invalid argument $1. Should be an integer.
        exit 1
    fi
else
    NUM_POSTS=20
fi

# Scrape some initial data
echo Sraping $PRIMARY_BLOG...
python3 main.py $PRIMARY_BLOG -n $NUM_POSTS

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
    python3 main.py $SINGLE_BLOG -n $NUM_POSTS
done

# Wait for the user to be done browsing
echo "Press return to terminate server"
read

clean_up
