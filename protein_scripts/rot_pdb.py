#!/usr/bin/python

# Imports
import pars_pdb
import numpy as np

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


def skew(v):                                                    # https://pythonpath.wordpress.com/2012/09/04/skew-with-numpy-operations/
    if len(v) == 4: v = v[:3]/v[3]
    skv = np.roll(np.roll(np.diag(v.flatten()), 1, 1), -1, 0)
    return skv - skv.T
def rotation_matrix(a,b):                                       # https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
    I = np.matrix([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]])
    # Get Norms 
    a_dist = np.linalg.norm(a)
    b_dist = np.linalg.norm(b)
    
    # Get unit Vectors
    a=a/a_dist
    b=b/b_dist
    
    v = np.cross(a,b)
    vx = skew(v)
    
    a_dist = np.linalg.norm(a)
    b_dist = np.linalg.norm(b)
    
    cos = np.dot(a,b.transpose())/(a_dist*b_dist)
    R = I + vx + np.matmul(vx,vx)*(1/(1+cos))
    return R

def rot_xyz(pdb_path,vec_from,vec_to):
    # Initialize Files
    pdb_old     = open(pdb_path)                                # Get  old PDB File
    pdb_new     = open(pdb_path[:-4]+"_rot.pdb","w+")           # Make new PDB File x-shift
    
    # Rotation Matrix
    R = rotation_matrix(vec_to,vec_from)
    
    for line in pdb_old:
        fields = line.strip().split()           # Splits Columns
        if(fields[0] == "ATOM"):                # Only Look at Atom Rows
            atom_prop_old = pars_pdb.line_to_pdb_atom(line)
            
            # Get xyz floats
            x_old   = float(atom_prop_old[8] )
            y_old   = float(atom_prop_old[9] )
            z_old   = float(atom_prop_old[10])
            vec_old = np.array([[x_old,y_old,z_old]])
            
            # Get New xyz floats
            vec_new = np.array(vec_old*R)[0]
            x_new = str(vec_new[0])
            y_new = str(vec_new[1])
            z_new = str(vec_new[2])
            
            # Get new lines
            atom_prop_new = atom_prop_old[:8]  + [x_new] + [y_new] + [z_new] + atom_prop_old[11:]
            new_line      = pars_pdb.pdb_atom_to_line( atom_prop_new )
            
            # Write New Lines
            pdb_new.write(new_line+"\n")
        else:
            pdb_new.write(line)
    pdb_old.close()
    pdb_new.close()

if (__name__ == "__main__"):
    pdb_path = os.path.abspath(sys.argv[1])                                             # Get PDB
    vec_from = np.array([[float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])]])   # Get Initial Vector
    vec_to   = np.array([[float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7])]])   # Get Resultant Vector
    rot_xyz(pdb_path,vec_from,vec_to)                                                   # Create Fix

