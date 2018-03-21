#!/usr/bin/python

# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def shift_xyz(pdb_path,x,y,z):
    # Initialize Files
    pdb_old     = open(pdb_path)                                # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_shift.pdb","w+")         # Make new PDB File x-shift
    
    for line in pdb_old:
        fields = line.strip().split()           # Splits Columns
        if(fields[0] == "ATOM"):                # Only Look at Atom Rows
            atom_prop_old = pdb_pars.line_to_pdb_atom(line)
            
            # Get xyz floats
            x_old = float(atom_prop_old[8] )
            y_old = float(atom_prop_old[9] )
            z_old = float(atom_prop_old[10])
            
            # Get new xyz str
            x_new = str(x_old + x)
            y_new = str(y_old + y)
            z_new = str(z_old + z)
            
            # Get new lines
            atom_prop_new = atom_prop_old[:8]  + [x_new] + [y_new] + [z_new] + atom_prop_old[11:]
            new_line      = pdb_pars.pdb_atom_to_line( atom_prop_new )
            
            # Write New Lines
            pdb_new.write(new_line+"\n")
        else:
            pdb_new.write(line)
    pdb_old.close()
    pdb_new.close()

if (__name__ == "__main__"):
    pdb_path    = os.path.abspath(sys.argv[1])          # Get PDB
    x           = float(sys.argv[2])                    # Get In Number
    y           = float(sys.argv[3])                    # Get In Number
    z           = float(sys.argv[4])                    # Get In Number
    shift_xyz(pdb_path,x,y,z)                           # Create Fix
