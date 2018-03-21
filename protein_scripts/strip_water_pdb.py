#!/usr/bin/python

# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def strip_water(pdb_path):
    # Initialize Files
    pdb_old     = open(pdb_path)                                    # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_stripped.pdb","w+")          # Make new PDB File
    
    # Variables
    last_line_water = False
    
    for line in pdb_old:
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Only Look at Atoms
            res_name = pdb_pars.line_to_pdb_atom(line)[4]                       # Residue Name
            if(res_name == "Na+" or res_name == "Cl-" or res_name == "WAT"):    # If Water or Ion
                last_line_water = True                                          #   Don't Write, and Remember.
            else:                                                               # Else
                pdb_new.write(line)                                             #   Write
                last_line_water = False
        elif(fields[0] == "TER"):                                               # If Terminal
            if(not last_line_water):                                            # And Not For Water
                pdb_new.write(line)                                             # Write
                last_line_water = False
        else:
            pdb_new.write(line)                                                 # Write
            last_line_water = False
    pdb_old.close()
    pdb_new.close()

if (__name__ == "__main__"):
    pdb_path    = os.path.abspath(sys.argv[1])                                  # Get PDB
    strip_water(pdb_path)