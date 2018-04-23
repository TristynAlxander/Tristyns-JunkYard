#!/usr/bin/python

# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys

## Select Atom Functions ##

def select_standard_residues(atom): # standard 
    standard_residue_list = ["ala","arg","asn","asp","cys" ,"gln" ,"glu" ,"gly","his","hse","ile","leu","lys","met","phe","pro","pyl","ser","sec","thr","trp","tyr","val"]
    return atom.res_name.lower() in standard_residue_list
    
def select_hydrogens_and_solvent(atom):
    return (
        atom.element  == "H" or 
        atom.chain_id == "W" or
        atom.chain_id == "I" or 
        atom.res_name == "TIP3"
        )

def select_hydrogens(atom):
    return atom.element == "H"

def select_hydrogens_solvent_and_residues(atom):
    return (
        select_hydrogens_and_solvent(atom) or 
        select_standard_residues(atom) and 
        not (atom.atom_name == "N" or atom.atom_name == "C" or atom.atom_name == "O" or atom.atom_name == "CA" )
        )

def select_all(atom):
    return True

def select_atoms(pdb_path_old,pdb_path_new,sel_func,atom_edit):
    # Initialize Files
    pdb_old  = open(pdb_path_old)                               # Get  old PDB File
    pdb_new  = open(pdb_path_new,"w+")                          # Make new PDB File
    
    for line in pdb_old:                                        # PDB line-by-line
        fields = line.strip().split()                           # Splits Columns
        if(fields[0] == "ATOM" or fields[0] == "HETATM" ):      # Only Look at Atom Rows
            atom = pars_pdb.Atom()                              # Make Atom
            atom.from_pdb_line(line)                            # Load Line into Atom
            
            if(sel_func(atom)):                                 # If Atom matches selection
                atom = atom_edit(atom)                     #   Edit Atom
            
            new_line = atom.to_pdb_line()                          # Rewrite Line
            pdb_new.write(new_line+"\n")                        # 
        else:                                   
            pdb_new.write(line)                                 # Write Non-Atoms
    
    # Close Files                                               # Close Files
    pdb_old.close()                                             # 
    pdb_new.close()                                             # 
    
    return pdb_path_new


    
## Edit Atom Functions ##

def free_temperature_factor(atom):
    atom.temp_factor = 0.0
    return atom
def fixed_temperature_factor(atom):
    atom.temp_factor = 1.0
    return atom
def repair_hydrogens(atom):
    if(atom.element == "" and atom.atom_name[0] == "H"):
        atom.element = "H"
    return atom


if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])          # Get PDB
    
    repaired_H_path = pdb_path[:-4]+"_H"+".pdb"         # 
    
    select_atoms(pdb_path,repaired_H_path,select_all,repair_hydrogens)
    
    all_fixed = "all_fixed.pdb" 
    select_atoms(repaired_H_path,all_fixed,select_all,fixed_temperature_factor)
    
    h_free = "h_free.pdb"         # 
    select_atoms(all_fixed,h_free,select_hydrogens,free_temperature_factor)
    
    h_h2o_free = "h_h2o_free.pdb"         # 
    select_atoms(all_fixed,h_h2o_free,select_hydrogens_and_solvent,free_temperature_factor)
    
    h_h2o_r_free = "h_h2o_r_free.pdb"
    select_atoms(all_fixed,h_h2o_r_free,select_hydrogens_solvent_and_residues,free_temperature_factor)
    
    
