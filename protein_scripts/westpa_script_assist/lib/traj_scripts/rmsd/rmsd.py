


### Imports ###

# Common Imports
import os
import sys

# System Specific Imports
import MDAnalysis
import MDAnalysis.analysis.rms
import numpy as np

### Common Functions ###

def has_required_files(txt="required.txt"):                     ### Checks for all files in txt. ###
    has_all_files  = True                                       # Assume All Exist Until Proven Wrong
    required_paths = open(txt)                                  # Open txt file
    for path in required_paths:                                 # Each line is a path
        path = path.strip()                                     # Strip Ends
        
        has_file = (                                            # Check File
            os.path.exists(path) and                            # If Not Exist, Add False
            os.path.isfile(path)                                # If Not File , Add False
            )                                                   # 
        
        has_all_files = (                                       # Reassign Boolean
            has_all_files and                                   # If Missing Other File, Keep False
            has_file                                            # If Missing This  File, Make False.
            )                                                   # 
        
        if(not has_file):                                       # For Missing Files
            print("Missing File: "+path)                        # Complain
    
    return has_all_files                                        # Return

def traj_to_list(traj_func, settings, *traj):                   ### Converts Trajectory(s) to List. ###
    out_list = []                                               # Start with Empty List
    for t in traj:                                              # For each trajectory
        out_list.extend(traj_func(settings,t))                  # Add Trajectory Outputs
    return out_list                                             # Return List

def w_traj_to_list(traj_func, settings, *traj):                 ### Converts Trajectory(s) to List for WestPA ###
    
    if(len(traj) == 1):                                         # Single List 
        return [traj_func(settings,traj[0])[-1]]                #   Returns Final Point 
    else:                                                       # Multiple Lists
        out_list = [traj_func(settings,traj[0])[-1]]            #   Start with the Final Point of First Trajectory
        for t in traj[1:]:                                      #   For other trajectories
            out_list.extend(traj_func(settings,t))              #   Add Full Trajectory Outputs
        return out_list                                         #   Return List

def list_to_dat(path,list):                                     ### Converts Lists to .dat ###
    file = open(path,"w+")                                      # Open File
    for item in list:                                           # For list item
        file.write(str(item)+"\n")                              # add line
    file.close()                                                # close file


### System Specific Functions ###

def get_rmsd(settings,traj,ref_pdb = "ref.pdb", my_psf = "my.psf"):
    
    system = MDAnalysis.Universe(my_psf,traj)
    ref = MDAnalysis.Universe(ref_pdb)
    
    R = MDAnalysis.analysis.rms.RMSD(system, ref,
           step=settings,
           select="backbone",           
           groupselections=["backbone"],
           filename="rmsd_backbone.dat")
    R.run()
    
    # rmsd[:,0]     # Count
    # rmsd[:,1]     # Time
    # rmsd[:,2]     # All
    # rmsd[:,3]     # groupselections 1
    # rmsd[:,...]   # groupselections ...
    
    return R.rmsd[:,3]

if (__name__ == "__main__"):
    
    if(   len(sys.argv) == 3 ):                                 ## Gather Inputs ##
        #this_script = os.path.abspath(sys.argv[0])             # Skip the Script
        trajectory_list =[                                      # Make Trajectory List
            os.path.abspath(sys.argv[1]),                       #    Parent  Path
            os.path.abspath(sys.argv[2])                        #    Segment Path
            ]                                                   #
    elif( len(sys.argv) == 2 ):
        #this_script = os.path.abspath(sys.argv[0])             # Skip the Script
        trajectory_list =[                                      # Make Trajectory List
            os.path.abspath(sys.argv[1])                        #    Parent  Path
            ]                                                   # 
    
    if(has_required_files()):
        my_list = w_traj_to_list(get_rmsd,10,*trajectory_list)
        print(my_list)
        print(len(my_list))
    
    
    
