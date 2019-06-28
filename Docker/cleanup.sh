#!/usr/bin/env bash

RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
RESET=`tput sgr0`
BOLD=`tput bold`

clean() {
    IMAGE=$(docker images | grep "<none>" | awk '{print $3}' )
    API_IMAGE=$(docker images | grep "api" | awk '{print $3}' )
    CONTAINERS=$(docker ps -a -q)
    VOLUME=$(docker volume ls | grep "airtech-api_tmp-docker_db" | awk '{print $2}')

    if [[ ! -z $CONTAINERS ]]; then
        echo $YELLOW$BOLD"==========[ Stop all running containers ]=========="$RESET
        docker stop $(docker ps -a -q)

        echo $YELLOW $BOLD"==========[ Remove all stopped containers ]=========="$RESET
        docker rm $(docker ps -a -q)
    fi


    if [[ ! -z $IMAGE ]]; then
        echo -e $YELLOW $BOLD"==========[ Remove all image with tag <none> ]=========="$RESET
        docker rmi -f $(docker images | grep "<none>" | awk '{print $3}')
    fi


    if [[ ! -z $API_IMAGE ]]; then
        echo $GREEN$BOLD"==========[ Remove API image ]=========="$RESET
        docker rmi airtech-api_api:latest
    fi


    if [[ -z $VOLUME ]]; then
        echo $RED$BOLD"==========[ No Volume Found. ]=========="$RESET
    else
        echo $GREEN$BOLD"==========[ Remove database volume. ]=========="$RESET
        docker volume rm airtech-api_tmp-docker_db
    fi
}

clean
