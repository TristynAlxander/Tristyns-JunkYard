# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


# Warning Doesn't Repair Terminals
def _cut_residues_start_end_(pdb_path,start,end):
    # Initialize Files
    pdb_old  = open(pdb_path)                                                   # Get  old PDB File
    new_name = pdb_path[:-4]+"_from_"+str(start)+"_to_"+str(end)+".pdb"         # 
    pdb_new  = open(new_name,"w+")                                              # Make new PDB File
    
    for line in pdb_old:                                                        # Iterate Through Lines
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Look at Atoms
            seq_num = int(pars_pdb.line_to_pdb_atom(line)[6])                   # Get Residue Sequence Number
            if( seq_num in range(start,end+1)):                                 # Write if in inclusive range 
                pdb_new.write(line)                                             #   
        elif(fields[0] == "TER"):                                               # Don't Write TER                               TODO: Fix Terminal?
            continue                                                            #
        else:                                                                   # Write Other Lines
            pdb_new.write(line)                                                 # 
    pdb_old.close()                                                             # Close Files 
    pdb_new.close()                                                             # 
    return new_name                                                             # Return File Name
    
def _cut_residues_start_(pdb_path,start):
    # Initialize Files
    pdb_old  = open(pdb_path)                                                   # Get  old PDB File
    new_name = pdb_path[:-4]+"_from_"+str(start)+".pdb"                         # 
    pdb_new  = open(new_name,"w+")                                              # Make new PDB File
    
    for line in pdb_old:                                                        # Iterate Through Lines
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Look at Atoms
            seq_num = int(pars_pdb.line_to_pdb_atom(line)[6])                   # Get Residue Sequence Number
            if( seq_num >= start):                                              # Write if in inclusive range
                pdb_new.write(line)                                             # 
        elif(fields[0] == "TER"):                                               # Don't Write TER                               TODO: Fix Terminal?
            continue                                                            #
        else:                                                                   # Write Other Lines
            pdb_new.write(line)                                                 # 
    pdb_old.close()                                                             # Close Files 
    pdb_new.close()                                                             # 
    return new_name                                                             # Return File Name
    
def _cut_residues_end_(pdb_path,end):
    # Initialize Files
    pdb_old  = open(pdb_path)                                                   # Get  old PDB File
    new_name = pdb_path[:-4]+"_to_"+str(end)+".pdb"                             # 
    pdb_new  = open(new_name,"w+")                                              # Make new PDB File
    
    for line in pdb_old:                                                        # Iterate Through Lines
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Look at Atoms
            seq_num = int(pars_pdb.line_to_pdb_atom(line)[6])                   # Get Residue Sequence Number
            if( seq_num <= end):                                                # Write if in inclusive range
                pdb_new.write(line)                                             # 
        elif(fields[0] == "TER"):                                               # Don't Write TER                               TODO: Fix Terminal?
            continue                                                            #
        else:                                                                   # Write Other Lines
            pdb_new.write(line)                                                 # 
    pdb_old.close()                                                             # Close Files 
    pdb_new.close()                                                             # 
    return new_name                                                             # Return File Name
    
def cut_residues(path,start=-1,end=-1):                                         # Select Correct Function
    name=""                                                                     # Default Name
    if(  start != -1 and end != -1):                                            # Start And End
        name = _cut_start_end_(path,start,end)                                  # 
    elif(start != -1):                                                          # Just Start
        name = _cut_start_(path,start)                                          # 
    elif(end   != -1):                                                          # Just End
        name = _cut_end_(path,end)                                              # 
    return name                                                                 # Return Name
        
if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                     # Get PDB
    i = int(sys.argv[2])                                                        # start
    j = int(sys.argv[3])                                                        # end
    cut_residues(pdb_path,i,j)
