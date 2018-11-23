#!/usr/bin/python

# Imports
import pars_pdb
import os

# Imports for Main
if (__name__ == "__main__"):
    import sys

def select_model(pdb_path,m):
    
    # Initialize Files
    pdb_old  = open(pdb_path)                                           # Get  old PDB File
    new_name = pdb_path[:-4]+"_m"+str(m)+".pdb"                         # 
    pdb_new  = open(new_name,"w+")                                      # Make new PDB File
    
    # Initialize Variables
    model_number = 0
    
    for line in pdb_old:
        fields = line.strip().split()                                   # Splits Columns
        if(fields[0] == "ATOM" or fields[0] == "HETATM"):               #
            
            if(model_number == m):                                      # If you're on the correct model
                pdb_new.write(line)                                     # Write the rows
            
        elif(fields[0] == "TER"):
            
            if(model_number == m):                                      # If you're on the correct model
                pdb_new.write(line)                                     # Write the rows
            
        elif(fields[0] == "MODEL"):
            model_number += 1
        elif(fields[0] == "ENDMDL"):
            continue
        else: 
            pdb_new.write(line)                 # Don't mess with non Atom non Model Rows 
    
    pdb_old.close()
    pdb_new.close()
    return new_name

def split_pdb(pdb_path,length):
    for i in range(0,length,1):
        select_model(pdb_path,i)
        
if (__name__ == "__main__"):
    split_pdb("all_pdb.pdb",251)