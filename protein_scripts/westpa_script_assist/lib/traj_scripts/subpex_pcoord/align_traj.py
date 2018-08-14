#!/usr/bin/env python

### 
### What this script does:
###   - Aligns Trajectories
###   - Strips Waters
###   - Converts to pdb
### 
### How to use Script:
###   - open terminal 
###   - python align_traj.py mol.psf parent.dcd child.dcd ref.pdb
###   - [Enter]
### 


# Imports
import MDAnalysis
from MDAnalysis.analysis import align
import os
import sys


# Functions                                                                                                 # Functions
def _align_trajectory_(traj, sel_str="name CA", pdb_filename=None):                                             # Align Trajectory Function
    
    # Get Reference                                                                                             # Get Reference
    ref = MDAnalysis.Universe(pdb_filename)                                                                     # Load Reference Structure
    sel_ref = ref.select_atoms(sel_str)                                                                         # Select Alignment Basis

    # Align Trajectory                                                                                          # Align Trajectory
    alignment = align.AlignTraj(traj, ref, in_memory=True, select=sel_str)                                      # Set Alignment Settings
    alignment.run()                                                                                             # Align
    
    # Return Aligned Trajectory                                                                                 # Return Aligned Trajectory
    return traj                                                                                                 # Return Aligned Trajectory


# Main                                                                                                      # Main
if __name__ == "__main__":
    # Load Files                                                                                                # Load Files
    psf         = os.path.abspath(sys.argv[1])                                                                  # System Parameters
    dcd_parent  = os.path.abspath(sys.argv[2])                                                                  # Parent Trajectory 
    dcd_child   = os.path.abspath(sys.argv[3])                                                                  # Child  Trajectory
    pdb_ref     = os.path.abspath(sys.argv[4])                                                                  # Reference Structure

    # Name Output                                                                                               # Name Output 
    pdb_out     = "temp/"+sys.argv[1][:-4]+'_aligned.pdb'                                                       # Add _aligned suffix

    # Get Trajectories                                                                                          # Get Trajectories  
    traj_parent = MDAnalysis.Universe(psf, dcd_parent)                                                          # Parent Trajectory 
    traj_child  = MDAnalysis.Universe(psf, dcd_child )                                                          # Child  Trajectory 

    # Align Trajectories                                                                                        # Align Trajectories
    traj_parent_aligned = _align_trajectory_(traj_parent,pdb_filename=pdb_ref)                                  # Parent Trajectory 
    traj_child_aligned  = _align_trajectory_(traj_child ,pdb_filename=pdb_ref)                                  # Child  Trajectory 


    # Save as PDB                                                                                               # Save as PDB
    with MDAnalysis.Writer(pdb_out, multiframe=True, bonds=None, n_atoms=traj_child_aligned.atoms.n_atoms) as PDB: # Writer "PDB"
        
        # Write Parent Trajectory                                                                               # Write Parent Trajectory
        parent_sel = traj_parent_aligned.select_atoms('protein')                                                # Strip Waters
        traj_parent_aligned.trajectory[-1]                                                                      # Last Frame Only
        PDB.write(parent_sel.atoms)                                                                             # Write Atoms
        
        # Write Child Trajectory                                                                                # Write Child Trajectory
        child_sel = traj_child_aligned.select_atoms('protein')                                                  # Strip Waters
        for ts in traj_child_aligned.trajectory:                                                                # Each Frame
            PDB.write(child_sel.atoms)                                                                          # Write Atoms
