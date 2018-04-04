# Imports
import MDAnalysis

if (__name__ == "__main__"):
    import sys
    import os

def first_pdb(system,pdb,sel_str="not segid SOLV"):                             ### Get First Trajectory ###
    system.select_atoms(sel_str).write(pdb)                                     # 

def last_pdb(system,pdb,sel_str="not segid SOLV"):                              ### Get Last Trajectory ###
    traj = system.trajectory                                                    # Get the Trajectory
    for i in range(0, len(traj)-1, 1):                                          # For all but the last Trajectory
        next(traj)                                                              #   Skip the Trajectory
    system.select_atoms(sel_str).write(pdb)                                     # Write PDB

def all_to_pdb(system,pdb,sel_str="not segid SOLV"):                            ### All Trajectory ###
    sel = system.select_atoms(sel_str)                                          # Select Atoms
    with MDAnalysis.Writer(pdb, multiframe=True, n_atoms=sel.n_atoms) as PDB:   # Make Writer
        for ts in system.trajectory:                                            # For each frame in Trajectory
            PDB.write(sel.atoms)                                                # Write Frame

if (__name__ == "__main__"):                                                    ### If Main ###
    psf    = os.path.abspath(sys.argv[1])                                       # PSF PATH
    dcd    = os.path.abspath(sys.argv[2])                                       # DCD PATH
    system = MDAnalysis.Universe(psf, dcd)                                      # Make Universe
    first_pdb(  system,"first_pdb.pdb")                                         # First PDB
    last_pdb(   system, "last_pdb.pdb")                                         # Last  PDB
    all_to_pdb( system,  "all_pdb.pdb")                                         # All   PDB
    

