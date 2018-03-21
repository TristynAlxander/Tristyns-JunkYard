# Imports
import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


# Warning Doesn't Repair Terminals
def strip_H(pdb_path,i,j):
    # Initialize Files
    pdb_old = open(pdb_path)                                                    # Get  old PDB File
    pdb_new = open(pdb_path[:-4]+"_"+str(i)+"_to_"+str(j)+".pdb","w+")          # Make new PDB File
    
    for line in pdb_old:
        fields = line.strip().split()                                           # Splits Columns
        if(fields[0] == "ATOM"):                                                # Only Look at Atoms
            seq_num = int(pars_pdb.line_to_pdb_atom(line)[6])                   # Residue Sequence Number
            if( seq_num in range(i,j)):                                         # If in range
                pdb_new.write(line)                                             #   Write
        elif(fields[0] == "TER"):                                               # If Terminal
            seq_num = int(pars_pdb.line_to_pdb_ter(line)[4])                    # Residue Sequence Number
            if( seq_num in range(i,j)):                                         # If in range
                pdb_new.write(line)                                             #   Write
        else:
            pdb_new.write(line)                                                 # Write
    pdb_old.close()
    pdb_new.close()

if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                     # Get PDB
    i = int(sys.argv[2])                                                        # start
    j = int(sys.argv[3])                                                        # end
    strip_H(pdb_path,i,j)