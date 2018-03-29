#!/usr/bin/python

# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def fix_b_range(pdb_path,i,j):
    
    # Initialize Files
    pdb_old     = open(pdb_path)                                    # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_"+str(i)+"_to_"+str(j)+".pdb","w+")    # Make new PDB File x-shift
    
    res_range   = range(i,j,1)
    
    for line in pdb_old:
        fields = line.strip().split()           # Splits Columns
        if(fields[0] == "ATOM"):                # Only Look at Atom Rows
            atom_prop_old = pars_pdb.line_to_pdb_atom(line)
            atom_name     = atom_prop_old[2]
            chain_name    = atom_prop_old[5]
            res_seq       = atom_prop_old[6]
            
            if(res_seq in res_range and atom_name == "CA"):
                atom_prop_new = atom_prop_old[:12]  + [1.00] + atom_prop_old[13:]
            else:
                atom_prop_new = atom_prop_old[:12]  + [0.00] + atom_prop_old[13:]
            
            # Get new lines
            new_line      = pars_pdb.pdb_atom_to_line( atom_prop_new )
            
            # Write New Lines
            pdb_new.write(new_line+"\n")
        else:
            pdb_new.write(line)
    pdb_old.close()
    pdb_new.close()

if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])         # Get PDB
    i = int(sys.argv[2])                            # Start
    j = int(sys.argv[3])                            # End+1
    fix_b_range(pdb_path,i,j)
    
