#!/usr/bin/python

# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def reseq(pdb_path):                                                    # WARNING: FLATTENS PDB FRAMES TO SUPERPOSITION, SO SPLIT MODELS FIRST.
    
    # Initialize Files
    pdb_old = open(pdb_path)                                            # Get  old PDB File
    pdb_new = open(pdb_path[:-4]+"_reseq.pdb","w+")                     # Make new PDB File
    
    # Initialize Residue Tracking Variables
    last_res_name       = ""                                            # No Initial Residue
    last_num_in         = ""                                            # No Initial Number
    last_chain          = ""                                            # No Initial Chain
    chain_num           = -1                                            # Start Number - 1 = -1
    res_seq             = 0                                             # Start Number - 1 = 0
    atom_num            = 0                                             # Start Number - 1 = 0
    res_change          = True                                          # Change Initial Residue    (Set here for scope)
    chain_change        = True                                          # Change Initial Chain      (Set here for scope)
    
    # Initialize Alphabet List
    alphabet = []                                                       # Empty List
    for letter in range(65, 91):                                        # Ascii Uppercase 
        alphabet.append(chr(letter))                                    # Make List
    
    
    for line in pdb_old:
        fields = line.strip().split()                                   # Splits Columns
        if(fields[0] == "ATOM" or fields[0] == "HETATM"):               # Only Look at Atom Rows
            
            atom_prop = pdb_pars.line_to_pdb_atom(line)                 # Covert to List
            
            # Detect Change in Residue
            new_res_name  = atom_prop[4] != last_res_name                # Detect Residue Name    Change
            new_res_num   = (atom_prop[6] + atom_prop[7]) != last_num_in # Detect Residue Number  Change
            res_change    = new_res_name or new_res_num                  # Either Implies Residue Change
            chain_change  = last_chain != atom_prop[5]                   # Detect Chain Change
            
            # Store Data for Next Line
            last_res_name = atom_prop[4]                                # Residue Type
            last_num_in   = atom_prop[6] + atom_prop[7]                 # Residue Number & Insertion Code
            last_chain    = atom_prop[5]                                # Chain
            
            # Resequence Residues
            if(res_change):                                             # If Residue Changed
                res_seq = res_seq + 1                                   #    Increment res_seq
            atom_prop[6] = str(res_seq)                                 # Set new_line's new res_seq
            atom_prop[7] = ""                                           # Strip Insertion Codes
            res_change  = False                                         # Reset Change in Residue Signal
            
            # Resequence Chains
            if(chain_change):
                chain_num = chain_num + 1                               # Increment Chain
            atom_prop[5]  = alphabet[chain_num]                         # Set Chain
            chain_change  = False                                       # Reset Chain Change Signal
            
            # Resequence Atoms
            atom_num    = atom_num + 1                                  # Increment atom_num
            atom_prop[1] = str(atom_num)                                # Set new atom_num
            
            # Write PDB
            new_line = pdb_pars.pdb_atom_to_line(atom_prop)             # Convert to String
            pdb_new.write(new_line+"\n")                                # Write Line to File
            
            
        elif(fields[0] == "TER"):
            
            atom_prop = pdb_pars.line_to_pdb_ter(line)                  # Covert to List
            
            # Detect Change in Residue
            new_res_name  = atom_prop[2] != last_res_name                # Detect Residue Name    Change
            new_res_num   = (atom_prop[4] + atom_prop[5]) != last_num_in  # Detect Residue Number  Change
            res_change    = new_res_name or new_res_num                 # Either Implies Residue Change
            chain_change  = last_chain != atom_prop[3]                   # Detect Chain Change
            
            # Store Data for Next Line
            last_res_name = atom_prop[2]                                 # Residue Type
            last_num_in   = atom_prop[4] + atom_prop[5]                   # Residue Number & Insertion Code
            last_chain    = atom_prop[3]                                 # Chain
            
            # Resequence Residues
            if(res_change):                                             # If Residue Changed
                res_seq = res_seq + 1                                   #     Increment res_seq
            atom_prop[4] = str(res_seq)                                  # Set new_line's new res_seq
            atom_prop[5] = ""                                            # Strip Insertion Codes
            res_change  = False                                         # Reset Change in Residue Signal
            
            # Resequence Atoms
            atom_num    = atom_num + 1                                  # Increment atom_num
            atom_prop[1] = str(atom_num)                                 # Set new atom_num
            
            # Resequence Chains
            if(chain_change):
                chain_num = chain_num + 1                               # Increment Chain
            atom_prop[3]   = alphabet[chain_num]                         # Set Chain
            chain_change  = False                                       # Reset Chain Change Signal
            
            # Write PDB
            new_line = pdb_pars.pdb_ter_to_line(atom_prop)              # Convert to String
            pdb_new.write(new_line+"\n")                                # Write Line to File
            
            
        elif(fields[0] == "MODEL"):
            continue
        elif(fields[0] == "ENDMDL"):
            continue
        else: 
            pdb_new.write(line)                 # Don't mess with non Atom Rows 
            res_change = True                   # Send res_change signal
    pdb_old.close()
    pdb_new.close()
if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])     # Get PDB
    reseq(pdb_path)
