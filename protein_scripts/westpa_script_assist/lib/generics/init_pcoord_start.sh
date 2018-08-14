#!/bin/bash


### START ###                                           #
                                                        #
if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging 
    set -x                                              # Display Commands
    env | sort                                          # Display Environment Variables (sorted)
fi                                                      #
                                                        #
source $WEST_SIM_ROOT/common/env.sh                     # Load Environmental Variables.
                                                        #
cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                        #
### /START ###                                          #


