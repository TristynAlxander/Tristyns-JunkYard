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




###  Segment Directory  ###
mkdir -pv $WEST_CURRENT_SEG_DATA_REF                                            # Make  Segment Directory
cd $WEST_CURRENT_SEG_DATA_REF                                                   # Go to Segment Directory

### Standard Files

### Parent Files  ###

### MD Files  ###
# Copy Config
# Run MD

###  Progress Coordinate  ###

###  Auxiliary Data  ###



###  Clean-Up  ###
rm -f \ 
