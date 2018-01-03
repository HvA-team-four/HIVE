#!/usr/bin/env bash

params="$(getopt -o hv: -l help,daemon,stop --name "$0" -- "$@")"
eval set -- "$params"

while [[ $# -gt 0 ]] ; do
    case $1 in
        -h|-\?|--help)
            echo "
####\    ####\   ####\  ###\          ###\  ############|
#### |   #### |  #### | ### \         ###|  ############|
#### |   #### |  #### |  ### \       ### /  #### |
############# |  #### |   ### \     ### /   #### |
############# |  #### |    ### \   ### /    ############| 
#### |   #### |  #### |     ### \ ### /     #### |
#### |   #### |  #### |      ### ### /      #### |
#### |   #### |  #### |       ##### /       ############|
####/    ####/   ####/         ###_/        ############/

HIVE application is created by FOUR.
Usage: bash HIVE.sh <options>

Startup:
    -h, --help         View help
    -d, --daemon       Start HIVE as daemon
    -s, --stop         Stop currently running daemons
            "
            exit 1
            ;;

        -d|--daemon)
            echo "
####\    ####\   ####\  ###\          ###\  ############|
#### |   #### |  #### | ### \         ###|  ############|
#### |   #### |  #### |  ### \       ### /  #### |
############# |  #### |   ### \     ### /   #### |
############# |  #### |    ### \   ### /    ############|
#### |   #### |  #### |     ### \ ### /     #### |
#### |   #### |  #### |      ### ### /      #### |
#### |   #### |  #### |       ##### /       ############|
####/    ####/   ####/         ###_/        ############/

HIVE application is created by FOUR.

This application has a EULA that needs your consent. Do you accept the EULA? (y/n)
            "
            read input
                if [ "$input" = y ] ; then
                    echo "EULA agreed, booting up HIVE as daemon"
                    source /opt/HIVE/bin/activate
                    circusd circus.ini
                   exit 1

                else
                    echo "EULA refused. Exiting..."
                    exit 1
                fi
            ;;

        -s|--stop)
            echo "Stopping HIVE deamon"
            source /opt/HIVE/bin/activate
            circusctl kill honeycomb
            circusctl kill ascout
            circusctl kill bee
            exit 1
         ;;


    esac
    shift
done

echo "
####\    ####\   ####\  ###\          ###\  ############|
#### |   #### |  #### | ### \         ###|  ############|
#### |   #### |  #### |  ### \       ### /  #### |
############# |  #### |   ### \     ### /   #### |
############# |  #### |    ### \   ### /    ############|
#### |   #### |  #### |     ### \ ### /     #### |
#### |   #### |  #### |      ### ### /      #### |
#### |   #### |  #### |       ##### /       ############|
####/    ####/   ####/         ###_/        ############/

HIVE application is created by FOUR.

This application has a EULA that needs your consent. Do you accept the EULA? (y/n)
"
            read input
                if [ "$input" = y ] ; then
                    echo "EULA agreed, booting up HIVE"
                    source /opt/HIVE/bin/activate
                    circusd circus.ini

                else
                    echo "EULA refused. Exiting..."
                    exit 1
                fi

