#!/usr/bin/python

# Imports
import pars_pdb
import os

# Imports for Main
if (__name__ == "__main__"):
    import sys


def split_pdb(pdb_path):
    # Initialize Files
    pdb_old     = open(pdb_path)                                    # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_0.pdb","w+")                 # Make new PDB File
    
    i = 0
    
    # Variables
    last_line_water = False
    
    for line in pdb_old:
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "END"):                                                 # Only Look at Atoms
            pdb_new.close()
            i=i+1
            pdb_new = open(pdb_path[:-4]+"_"+str(i)+".pdb","w+")                # Make new PDB File
        else:
            pdb_new.write(line)                                                 # Write
    
    pdb_old.close()
    pdb_new.close()
    os.remove(pdb_path[:-4]+"_"+str(i)+".pdb")
    
if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                     # Get PDB
    split_pdb(pdb_path)