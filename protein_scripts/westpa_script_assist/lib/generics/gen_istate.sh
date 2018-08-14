#!/bin/bash

### START ###                                           #
                                                        #
if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging 
    set -x                                              # Display Commands
    env | sort                                          # Display Environment Variables (sorts)
fi                                                      #
                                                        #
source $WEST_SIM_ROOT/common/env.sh                     # Load Environmental Variables.
                                                        #
cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                        #
### /START ###                                          #


### Link Bstates
mkdir -p $(dirname $WEST_ISTATE_DATA_REF)           # Make Directory (with parents, as needed) of Path
ln -s $WEST_BSTATE_DATA_REF $WEST_ISTATE_DATA_REF   # Symlinking original(basis states) new(initial states)
