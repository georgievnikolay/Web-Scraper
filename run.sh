#!/bin/bash

PRIMARY_BLOG='travelsmart' 
EXTRA_BLOGS=('bozho' 'az_moga' 'igicheva' 'pateshestvenik')

echo Sraping $PRIMARY_BLOG...
python3 main.py $PRIMARY_BLOG

python3 web_instance.py >/dev/null 2>/dev/null &
xdg-open http://127.0.0.1:5000/

for SINGLE_BLOG in ${EXTRA_BLOGS[@]}
do
    echo Sraping $SINGLE_BLOG...
    python3 main.py $SINGLE_BLOG
done

echo "Press return to terminate server"
read

kill -9 $(lsof -ti tcp:5000)
