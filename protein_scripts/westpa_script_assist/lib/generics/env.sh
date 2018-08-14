#!/bin/sh
################################## WESTPA #######################################
# Is WEST_ROOT set?                                                             #
if [ -z "$WEST_ROOT" ]; then                                                    #
  echo "The environment variable WEST_ROOT is not set."                         #
  echo "Try running 'source westpa.sh' from the WESTPA installation directory"  #
  exit 1                                                                        #
fi                                                                              #
                                                                                #
# If no Simulation Root Directory, make it current Directory                    #
if [ -z "$WEST_SIM_ROOT" ]; then                                                #
  export WEST_SIM_ROOT="$PWD"                                                   #
fi                                                                              #
                                                                                #
export SIM_NAME=$(basename $WEST_SIM_ROOT)                                      #
                                                                                #
#################################################################################

