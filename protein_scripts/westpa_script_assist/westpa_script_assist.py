
# Imports
import os
import sys
from datetime import datetime           # For naming westpa scripts directory
import shutil                           # For Copying Generics 

#import importlib.util
#env_spec = importlib.util.spec_from_file_location("module.name", "lib/classes/env.py")
#env_mod  = importlib.util.module_from_spec(env_spec)
#env_spec.loader.exec_module(env_mod)

# Add My Scripts File to Path                                       # Add My Scripts File to Path
current_dir     = os.path.dirname(os.path.realpath(__file__))+"/"   # 
westpa_classes  = current_dir+"lib/classes/"                        # 
sys.path.insert(0, westpa_classes)                                  # 

import env
import bstates
import traj_scripts
#import init_states
#westpa_scr_dir = "westpa_sim_root_"+time_string


def new_sim_root():
    
    ### Westpa Simulation Root ###
    
    # Directory                                                                     # Directory 
    time_string         = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')              # Time as String
    westpa_sim_root_dir = "westpa_sim_root_"+time_string                            # Directory Name
    if not os.path.exists(westpa_sim_root_dir):                                     # 
        os.makedirs(westpa_sim_root_dir)                                            # Make Directory
    
    # Scripts
    shutil.copyfile("lib/generics/west.cfg", westpa_sim_root_dir+"/west.cfg")           # Westpa Configuration 
    shutil.copyfile("lib/generics/run.sh",   westpa_sim_root_dir+"/run.sh")             # Run
    
    
    
    
    ### Initial States ###
    
    # Initiate Script                                                               # Initiate Script
    shutil.copyfile("lib/generics/init.sh", westpa_sim_root_dir+"/init.sh")             # 
    
    # Initial Directory                                                             # Initial Directory 
    init_states_dir = westpa_sim_root_dir+"/init_states"                            # Directory Name
    if not os.path.exists(init_states_dir):                                         #
        os.makedirs(init_states_dir)                                                # Make Directory
    
    # Initial States                                                                    # Initial States
    shutil.copyfile("lib/generics/gen_istate.sh", init_states_dir+"/gen_istate.sh")         # Make Initial States 
    shutil.copyfile("lib/generics/init_pcoord_start.sh", init_states_dir+"/init_pcoord.sh") # Make Initial Progress Coordinates
    
    ### Segments ###
    
    # Segment Directory                                                             # Segment Directory 
    seg_scripts_dir = westpa_sim_root_dir+"/seg_scripts"                            # Directory Name
    if not os.path.exists(seg_scripts_dir):                                         #
        os.makedirs(seg_scripts_dir)                                                # Make Directory
    
    # Segment Scripts                                                               # Segment Scripts
    shutil.copyfile("lib/generics/pre_iter.sh",  seg_scripts_dir+"/pre_iter.sh")        # Pre
    shutil.copyfile("lib/generics/runseg.sh",    seg_scripts_dir+"/runseg.sh")          # Run
    shutil.copyfile("lib/generics/post_iter.sh", seg_scripts_dir+"/post_iter.sh")       # Post
    
    return westpa_sim_root_dir


def cap_files(westpa_sim_root_dir):
    
    # Cap init_pcoord.sh File                                                       # Cap init_pcoord.sh File
    init_pcoord     = open(westpa_sim_root_dir+"/init_states/init_pcoord.sh","a")   # Open for Append
    init_pcoord_end = open("lib/generics/init_pcoord_end.sh","r")                   # Open for Read
    for line in init_pcoord_end:                                                    # For Each Cap Line
        init_pcoord.write(line)                                                     # Write to File
    init_pcoord_end.close()                                                         # Close Cap
    init_pcoord.close()                                                             # Close File


def fix_file_path(file_path):
    file_path = file_path.replace("\\","/")                                             # Fix Slashes
    
    if(":" in file_path[:2]):                                                           # If Bad Drive        E.g:  D:/
        new_drive = "/mnt/"+file_path[:2].replace(":","").lower()                       #   Fix Drive Prefix  E.g:  /mnt/d
        file_path = new_drive+file_path[2:]                                             #   Fix Path
    
    file_name   = file_path.split("/")[-1]                                              # Isolate File Name
    if("." in file_name):
        dot_index   = file_name.find(".")                                               # Find start of suffix 
        file_suffix = file_name[dot_index:]                                             # Isolate suffix
    else:
        file_suffix = file_name
    
    return (file_path,file_name,file_suffix)


def add_eq_files(westpa_sim_root_dir,*files):
    
    # Variables                                                                     # Variables 
    initial_states_dir = westpa_sim_root_dir+"/init_states/basis_states/initial"    # TODO: Learn how multiple initial states work
    hashes = "#################################"                                    # 
    
    # Title Equilibrium Files Section in init_pcoord.sh File                        # Title Section
    init_pcoord_sh = open(westpa_sim_root_dir+"/init_states/init_pcoord.sh","a")     # Open for Append
    init_pcoord_sh.write(hashes+" Equilibrium Files "+hashes+"\n")                  # Append Title
    
    
    # Process Files                                                                 # Process Files
    for file_path in files:                                                         # For each file path
        
        ### Copy Common Files ###                                                       ### Copy Common Files ###
        
        path_fix    = fix_file_path(file_path)                                              # Fix File Path
        file_path   = path_fix[0]                                                           # Get Path
        file_name   = path_fix[1]                                                           # Get Name
        file_suffix = path_fix[2]                                                           # Get Suffix
        
        shutil.copyfile(file_path, initial_states_dir+"/seg"+file_suffix)                       # Copy File as first segment
        
        
        ### Link Files in Initial Progress Coordinates ###                              ### Link Files in Initial Progress Coordinates ###
        from_location = "$WEST_SIM_ROOT/init_states/basis_states/initial/seg"+file_suffix   # From Path Location
        to_location   = "$WEST_SIM_ROOT/init_states/init_pcoord/"                           # To   Path Location
        link_line     = "ln -sf "+from_location+"    "+to_location+" || exit 1\n"           # Link Statement
        init_pcoord_sh.write(link_line)                                                     # Write to init_pcoord.sh
        
    # Close File                                                                    # Close File
    init_pcoord_sh.close()                                                          # Close init_pcoord.sh 
    

def add_p_coord(westpa_sim_root_dir, pcoord_dir):
    
    i=0                                                                             # Start Count
    westpa_pcoord_dir = westpa_sim_root_dir+"/pcoord/"+str(i)+"_pcoord"             # Define Progress Coordinate Directory
    while(os.path.exists(westpa_pcoord_dir)):                                       # while the name is still taken
        i=i+1                                                                       # Increment Count 
        westpa_pcoord_dir = westpa_sim_root_dir+"/pcoord/"+str(i)+"_pcoord"         # Define Progress Coordinate Directory
    shutil.copytree(pcoord_dir, westpa_pcoord_dir)                                  # Copy Directory
    
    ### Link Files in Initial Progress Coordinates ###                              ### Link Files in Initial Progress Coordinates ###
    # Title Common Files Section in init.sh File                                    # Title Section
    init_pcoord_sh = open(westpa_sim_root_dir+"/init_states/init_pcoord.sh","a")    # Open for Append
    hashes = "#################################"                                    # 
    init_pcoord_sh.write(hashes+" Common Files "+hashes+"\n")                       # Append Title
    
    for dirpath, dirnames, filenames in os.walk(westpa_pcoord_dir):
        for file in filenames:
            file_path = dirpath+"/"+file                                                        # Get full path
            i = file_path.find(westpa_sim_root_dir)+len(westpa_sim_root_dir)                    # index after root
            
            from_location = "$WEST_SIM_ROOT"+file_path[i:]                                      # From Path Location
            to_location   = "$WEST_SIM_ROOT/i2nit_states/init_pcoord/"                           # To   Path Location
            link_line     = "ln -sf "+from_location+"    "+to_location+" || exit 1\n"           # Link Statement
            init_pcoord_sh.write(link_line)                                                     # Write to init_pcoord.sh
            
    init_pcoord_sh.close()                                                          # Close init_pcoord.sh 
    



westpa_sim_root_dir = new_sim_root()
### Make Files

print(westpa_sim_root_dir)



### Environment Files ##

env_prmtop = "lib/test_files/mol.prmtop"
env_psf    = "lib/test_files/mol.psf"
env_pdb    = "lib/test_files/mol.pdb"
env_inpcrd = "lib/test_files/mol.inpcrd"
env_path_array = [env_prmtop, env_psf, env_pdb, env_inpcrd]

my_env = env.Env(westpa_sim_root_dir)
my_env.env_paths = env_path_array
my_env.make_env_scripts()



### Basis State Files ###

bstate_coor = "lib/test_files/mol.coor"
bstate_vel  = "lib/test_files/mol.vel"
bstate_xsc  = "lib/test_files/mol.xsc"
bstate_dcd  = "lib/test_files/mol.dcd"
bstates_path_array = [bstate_coor,bstate_vel,bstate_xsc,bstate_dcd]

my_bstates = bstates.BStates(westpa_sim_root_dir)
my_bstates.bstate_paths = bstates_path_array
my_bstates.make_bstates_scripts()



### Trajectory State Files ###

pcoord_dirs = ["lib/traj_scripts/rmsd"]
aux_dirs    = ["lib/traj_scripts/rmsd"]

traj_scripts     = traj_scripts.TrajScripts(westpa_sim_root_dir)
traj_scripts.env = my_env

traj_scripts.pcoord_dirs = pcoord_dirs
traj_scripts.__prep_pcoord_files__()

traj_scripts.aux_dirs    = aux_dirs
traj_scripts.__prep_aux_files__()

traj_scripts.make_traj_scripts()

