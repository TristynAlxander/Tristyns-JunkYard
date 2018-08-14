#!/bin/bash



#### Prepare Temporary Space ####
rm -rf temp
mkdir temp


#################### Trajectory to PDB ####################

python2 align_traj.py mol.psf parent.dcd seg.dcd ref.pdb

python2 to_traj_pdb.py temp/mol_aligned.pdb

#################### SubPEX ####################

# Check Chain for SubPEX Settings
python2 fix_settings.py temp/mol_aligned_traj.pdb

# Run SubPEX
python2 SubPEX_tweaked.py


#################### Jaccard Index #################### 

# Run Conversion
python2 jindex.py > pcoord_temp.txt


#### Delete Temporary Space ####
rm -rf temp                        # TODO: Un-Comment-Out
