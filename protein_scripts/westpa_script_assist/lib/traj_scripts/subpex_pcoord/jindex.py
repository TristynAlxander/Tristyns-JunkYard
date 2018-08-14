# Import Statements
import numpy  as np
import pandas as pd
import cStringIO
import os.path
import sys
import os

def xyz_to_npa(path):
    # Read File
    file     = open(path,"r")                                                           # Open  File
    lines    = file.readlines()                                                         # Read  File
    file.close()                                                                        # Close File
    file_str = cStringIO.StringIO("".join(lines[2:-1]))                                 # Keep Third Line to Last Line
    
    
    #Make Numpy Array
    df = pd.read_csv(file_str, delim_whitespace=True, header=None, usecols=[1,2,3])     # Ignore First Column
    npa_array = df.as_matrix()                                                          # Convert to Matrix
    
    return npa_array                                                                    # Return


def jaccard_index_2d(A,B):
    # Get Intersect
    a_nrows, a_ncols = A.shape                                                          # Get Shape
    b_nrows, b_ncols = B.shape                                                          # Get Shape
    if(a_ncols == 3 and b_ncols == 3):
        C = []
        for a_row in A.astype('float32'):
            C.append("{0},{1},{2}".format(a_row[0],a_row[1],a_row[2]))
        D = []
        for b_row in B.astype('float32'):
            D.append("{0},{1},{2}".format(b_row[0],b_row[1],b_row[2]))
        E = np.intersect1d(C, D)
        return len(E)*1.0/(len(C)+len(D)-len(E))
    else: 
        return None
    
# Get pcoords 
ref_npa = xyz_to_npa("ref.xyz")                                         # Reference File

i=0                                                                     # Index
while(  os.path.isfile("temp/mol_aligned_traj_frame"+str(i)+".xyz")  ): # While next frame exists
    i_npa = xyz_to_npa("temp/mol_aligned_traj_frame"+str(i)+".xyz")     # Convert to NumPy Array
    jindex = jaccard_index_2d(ref_npa,i_npa)                            # Convert to Jaccard Index
    print("{:.05f}".format(jindex))                                     # Output
    i=i+1


