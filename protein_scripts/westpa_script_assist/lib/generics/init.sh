#!/bin/bash
#
# init.sh
#
# Creates initial-states (istates) 
# Creates WESTPA data file: west.h5. 
#

### Imports ###
###################################### Imports ######################################
source $WEST_SIM_ROOT/common/env.sh                                                 # Load Environmental Variables.
cd $WEST_SIM_ROOT

##################################### Clean-Up #####################################
pkill -9 -f w_run                                                                   # Kill All Other WESTPA Instances
rm -rf traj_segs seg_logs ./init_states/istates west.h5 || exit 1                   # Remove Directories
mkdir  traj_segs seg_logs ./init_states/istates         || exit 1                   # Remake Directories

################################ Run Westpa's w_init ################################

# Must be in WEST_SIM_ROOT when you run this.
cd $WEST_SIM_ROOT

# Define Arguments
BSTATE_ARGS="--bstate-file init_states/basis_states/bstates.txt"                         # Define Basis  States
#TSTATE_ARGS="--tstate target,1.0"                                                  # Define Target States

# Initialize the simulation, creating the main WESTPA data file (west.h5)
# The "$@" lets us take any arguments that were passed to init.sh at the command line and pass them along to w_init.
$WEST_ROOT/bin/w_init \
  $BSTATE_ARGS $TSTATE_ARGS \
  --segs-per-state 5 \
  --work-manager=threads "$@"