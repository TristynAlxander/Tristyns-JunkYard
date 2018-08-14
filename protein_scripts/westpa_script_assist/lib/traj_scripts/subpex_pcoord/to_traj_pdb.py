#!/usr/bin/python

### 
### What this script does:
###   - Converts PDB Models into PDB Frames
### 
### How to use Script:
###   - open terminal 
###   - python to_traj_pdb.py mol.pdb
###   - [Enter]
### 


# Imports for Main
if (__name__ == "__main__"):
    import sys
    import os


# Functions                                                     # Functions
def to_traj(pdb_path):
    
    # Initialize Files                                              # Initialize Files
    pdb_old     = open(pdb_path)                                    # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_traj.pdb","w+")              # Make new PDB File
    
    # Variables                                                     # Variables
    first_model = True                                              # Track First Model
    
    for line in pdb_old:                                            # For Each Line
        fields = line.strip().split()                               # Split to Columns
        
        if(fields[0] == "MODEL"):                                   # At Model Start, Delete Model (Don't Write)
            if(not first_model):                                    # If not first model, end frame.
                pdb_new.write("END\n")                              # End Frame
                continue                                            # Delete Model (Don't Write)
            else:                                                   # If First Model
                first_model = False                                 # Note Change 
                continue                                            # Delete Model (Don't Write)
        elif(fields[0] == "ENDMDL"):                                # At Model End, Delete Model (Don't Write)
            continue                                                # Delete Model (Don't Write)
        else:                                                       # Anything Else, Leave Alone
            pdb_new.write(line)                                     # Leave Alone (Write)
    
    pdb_old.close()                                                 # Close Old PDB
    pdb_new.close()                                                 # Close New PDB


# Main                                                          # Main
if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                         # Get PDB
    to_traj(pdb_path)                                               # Convert to Trajectory