#!/usr/bin/env bash

RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BOLD=`tput bold`

database_setups(){
    python manage.py checkDB
    python manage.py migrate
    python manage.py collectstatic --noinput
    sleep 2
}


API_startup() {

    gunicorn --access-logfile '-' \
        --workers 2 --timeout 3600 \
        src.wsgi:application --bind 0.0.0.0:9000 --reload \
        --access-logformat "%(h)s %(u)s %(t)s '%(r)s' %(s)s '%(f)s' '%(a)s'"
}

main() {

    # Set up the database
    echo -e "\n \n"
    echo $YELLOW$BOLD"==========[ Setting up the database. ]=========="
    database_setups
    sleep 2

    # Start server
    echo -e "\n \n"
    echo $GREEN$BOLD"==========[ Starting the server ]=========="
    API_startup
}

main
