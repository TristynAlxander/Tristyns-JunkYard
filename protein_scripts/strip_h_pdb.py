# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def strip_H(pdb_path):
    # Initialize Files
    pdb_old = open(pdb_path)                                                    # Get  old PDB File
    new_name = pdb_path[:-4]+"_strip_h.pdb"                                     # 
    pdb_new  = open(new_name,"w+")                                              # Make new PDB File
    
    for line in pdb_old:
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Only Look at Atoms
            atom_name = pars_pdb.line_to_pdb_atom(line)[2].strip()              # Atom Name
            if( not atom_name[0] == "H"):                                        # If not Hydrogen
                pdb_new.write(line)                                             #   Write
        else:
            pdb_new.write(line)                                                 # Write
    pdb_old.close()
    pdb_new.close()
    return new_name

if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                     # Get PDB
    strip_H(pdb_path)
