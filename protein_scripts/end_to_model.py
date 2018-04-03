# Imports
#import pars_pdb

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


def end_to_model(pdb_path):                                                             # Convert End Separated to Model Separated
    
    # Initialize Files
    pdb_old = open(pdb_path)                                                            # Get  old PDB File
    pdb_new = open(pdb_path[:-4]+"_models.pdb","w+")                                    # Make new PDB File
    
    # Initial Model Settings                                                            # Initial Model Settings 
    model_num = 0                                                                       # Model Number
    in_model  = False                                                                   # Starts outside the model
    
    for line in pdb_old:
        fields = line.strip().split()                                                   # Splits Columns
        if(fields[0] == "ATOM" or fields[0] == "HETATM"):                               # Only Look at Atom Rows
            if(not in_model):                                                           #   If we weren't already in a model
                model_num = model_num + 1                                               #   Start New Model
                model_line = "{0:<6.6}    {1:>4.4}\n".format("MODEL",str(model_num))    #   Create model line
                pdb_new.write(model_line)                                               #   write line
                pdb_new.write(line)                                                     #   write atom too
                in_model = True                                                         #   We're now in a model 
            else:
                pdb_new.write(line)
        elif(fields[0] == "END"):                                                       # At Breaks
            pdb_new.write("ENDMDL\n")                                                   #   End model
            in_model = False                                                            #   No longer in a model
        elif(fields[0] == "MODEL"):
            pdb_new.write(line)
        elif(fields[0] == "ENDMDL"):
            pdb_new.write(line)
    
    pdb_new.write("END")                                                                # End of File
    pdb_new.close()                                                                     # 
    
if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                             # Get PDB
    end_to_model(pdb_path)