#!/usr/bin/env bash

RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BOLD=`tput bold`

database_setups(){
    python manage.py checkDB
    python manage.py migrate --run-syncdb
    python manage.py collectstatic --noinput
    sleep 2
}


API_startup() {

    # Celery
    celery worker -A src.celery --loglevel=info --concurrency=4 &
    celery -A src.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile=/tmp/celeryd.pid &
    celery flower -A src.celery --address=0.0.0.0 --port=5555 &
    sleep 5

    # Start server
    echo -e "\n \n"
    gunicorn --access-logfile '-' \
        --workers 2 --timeout 3600 \
        src.wsgi:application --bind 0.0.0.0:$PORT --reload \
        --access-logformat "%(h)s %(u)s %(t)s '%(r)s' %(s)s '%(f)s' '%(a)s'"
}

main() {

    # Set up the database
    echo -e "\n \n"
    echo $YELLOW$BOLD"==========[ Database ]=========="
    database_setups
    sleep 2

    # Start server
    echo -e "\n \n"
    echo $GREEN$BOLD"==========[ Server ]=========="
    API_startup
}

main
