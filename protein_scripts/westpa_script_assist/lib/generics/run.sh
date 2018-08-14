#!/bin/bash

source $WEST_SIM_ROOT/common/env.sh                             # Load Environmental Variables.

rm -f west.log                                                  # Clean previous west.log's
$WEST_ROOT/bin/w_run --work-manager processes "$@" &> west.log  # Create new west.log's
