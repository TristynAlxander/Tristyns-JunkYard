# Imports
#import pars_pdb
import MDAnalysis
import numpy as np
import math

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


def vector_projection(a,b,debug=False):
    # Vector Projection Equation:
    #   \text{proj}_{\vec{b}} \vec{a}  = \frac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2} \vec{b}
    #
    
    ### Debug / Break / Fix ###                                                                 ### Debug / Break / Fix ###
    if(debug):
        if(not (type(a) is list or type(a) is np.matrix)):                                      # Verify vector A is list or matrix
            print("Vector Projection: First Input is Invalid Type.")                            # 
            return None                                                                         # 
        elif(not (type(b) is list or type(b) is np.matrix)):                                    # Verify vector B is list or matrix
            print("Vector Projection: Second Input is Invalid Type.")                           # 
            return None                                                                         # 
        else:
            if(type(a) is list):                                                                # Make Lists into Matrix
                a =  np.matrix(a)                                                               # 
                print("First List should be Matrix.")                                           # 
            if(type(b) is list):                                                                # 
                b =  np.matrix(b)                                                               # 
                print("Second List should be Matrix.")                                          # 
            
            if(a.size != b.size):                                                               # Verify Vectors are the same size
                print("Vector Projection: Inputs must have same size" )                         # 
                print("First Vector, size " +str(a.size)+":\n"+str(a) )                         # 
                print("Second Vector, size "+str(b.size)+":\n"+str(b) )                         # 
                return None                                                                     # 
            
            if( (len(a.shape) != 2) or (not 1 in a.shape)):                                     # Verify Vectors have useful shape
                print("Vector Projection: First Vector has improper shape: " +str(a.shape))     # 
                return None                                                                     # 
            if( (len(b.shape) != 2) or (not 1 in b.shape)):                                     # 
                print("Vector Projection: Second Vector has improper shape: "+str(b.shape))     # 
                return None                                                                     #
            
            if(a.shape[0] != 1):                                                                # Correct Transposed Shapes
                a = a.transpose()                                                               # 
                print("First Vector Needed to be transposed.")                                  #
            if(b.shape[0] != 1):                                                                # 
                b = b.transpose()                                                               # 
                print("Second Vector Needed to be transposed.")                                 # 
    
    ### Calculate Projection ###                                                                ### Calculate Projection ###
    
    numerator   = np.dot(a,b.transpose())                                                       # Dot Products
    denominator = np.dot(b,b.transpose())                                                       #
    
    numerator   = float(numerator)                                                              # Cast to Float
    denominator = float(denominator)                                                            # 
    
    scalar = numerator/denominator                                                              # Calculate Scalar
    
    solution = np.inner(scalar,b)                                                               # Calculate Solution
    return solution                                                                             # Return Solution

def plane_projection(a,normal,debug=False):
    # Plane Projection Equation:
    #   \text{proj}_{P} \vec{a}  = \vec{a} - \text{proj}_{\vec{n}} \vec{a}
    #   
    #   Where \vec{n} is the normal vector to plane P
    # 
    
    
    ### Debug / Break / Fix ###                                                             ### Debug / Break / Fix ###
    if(debug):
        if(not (type(a) is list or type(a) is np.matrix)):                                      # Verify vector A is list or matrix
            print("Vector Projection: First Input is Invalid Type.")                            # 
            return None                                                                         # 
        elif(not (type(normal) is list or type(normal) is np.matrix)):                          # Verify vector B is list or matrix
            print("Vector Projection: Normal Vector is Invalid Type.")                          # 
            return None                                                                         # 
        else:
            if(type(a) is list):                                                                # Make Lists into Matrix
                a =  np.matrix(a)                                                               # 
                print("First List should be Matrix.")                                           # 
            if(type(normal) is list):                                                           # 
                normal =  np.matrix(normal)                                                     # 
                print("Normal List should be Matrix.")                                          # 
            
            if(a.size != normal.size):                                                          # Verify Vectors are the same size
                print("Vector Projection: Inputs must have same size" )                         # 
                print("First Vector, size " +str(a.size)+":\n"+str(a) )                         # 
                print("Normal Vector, size "+str(normal.size)+":\n"+str(normal) )               # 
                return None                                                                     # 
            
            if( (len(a.shape) != 2) or (not 1 in a.shape)):                                     # Verify Vectors have useful shape
                print("Vector Projection: First Vector has improper shape: " +str(a.shape))     # 
                return None                                                                     # 
            if( (len(normal.shape) != 2) or (not 1 in normal.shape)):                           # 
                print("Vector Projection: Normal Vector has improper shape: "+str(b.shape))     # 
                return None                                                                     #
            
            if(a.shape[0] != 1):                                                                # Correct Transposed Shapes
                a = a.transpose()                                                               # 
                print("First Vector Needed to be transposed.")                                  #
            if(normal.shape[0] != 1):                                                           # 
                normal = normal.transpose()                                                     # 
                print("Normal Vector Needed to be transposed.")                                 # 
    
    ### Calculate Projection ###                                                                ### Calculate Projection ###
    return np.subtract(a,vector_projection(a,normal))

def dihedral_angle(a,b,c,d):
    # Given Dihedral 
    #  a       d
    #   \     /
    #    b---c
    #
    # Projection Plane
    #  a             d
    #   \           /
    #    \    |    /
    #     b---|---c
    #  front  |  back
    #
    #  Testing Example
    #  <--- z-axis --->
    #  a             d
    #   \           /
    #    \    |    /
    #     b---|---c
    #         |
    #      x,y-plane
    """
    # To Test Replace x,y with unit circle values
    #               x  y  z
    a =  np.matrix([0, 1, 1])
    b =  np.matrix([0, 0, 2])
    c =  np.matrix([0, 0, 4])
    d =  np.matrix([x, y, 5])
    """
    
    b_to_a            = np.subtract(b,a)                                            # Get Appropriate Vectors
    b_to_c            = np.subtract(b,c)                                            # 
    c_to_b            = np.subtract(c,b)                                            # 
    c_to_d            = np.subtract(c,d)                                            # 
    
    perpendicular     = c_to_b                                                      # TODO: Is this the right perpendicular? c_to_b
    
    unit_normal       = np.dot(perpendicular , 1/np.linalg.norm(perpendicular) )    # Unit Normal, to make everything a scale properly.
    
    front_projection  = plane_projection( b_to_a , unit_normal )                    # Front & Back Projections
    back_projection   = plane_projection( c_to_d , unit_normal )                    # See Diagram above. 
    
    cross_product    = np.cross(front_projection,back_projection)                   # Sine component of the determinant
    determinant      = np.dot(unit_normal,cross_product.transpose())                # Determinant is proportional to sine
    dot_product      = np.dot(front_projection,back_projection.transpose())         # Dot-Product is proportional to cosine
    
    theta = math.atan2(determinant, dot_product)                                    # Get Angle
    
    return theta


def get_phi_angle( system, res_index ):
    ### Selection Syntax to Select Atoms ###                                                ### Selection Syntax to Select Atoms ###
    atom_C0 = system.select_atoms("name C  and resid " + str(res_index-1))[0]               # 
    atom_N  = system.select_atoms("name N  and resid " + str(res_index  ))[0]               # 
    atom_CA = system.select_atoms("name CA and resid " + str(res_index  ))[0]               # 
    atom_C1 = system.select_atoms("name C  and resid " + str(res_index  ))[0]               # 
    
    dihedral_angle_list = []                                                                # Assemble List of Dihedral Angles
    for ts in system.trajectory:                                                            # 
        dihedral_angle_list.append( dihedral_angle(atom_C0.position, atom_N.position, atom_CA.position, atom_C1.position) )
    return dihedral_angle_list                                                              # 

def get_psi_angle( system, res_index ):
    ### Selection Syntax to Select Atoms ###                                                ### Selection Syntax to Select Atoms ###
    atom_N  = system.select_atoms("name N  and resid " + str(res_index  ))[0]               # 
    atom_CA = system.select_atoms("name CA and resid " + str(res_index  ))[0]               # 
    atom_C0 = system.select_atoms("name C  and resid " + str(res_index  ))[0]               # 
    atom_N1 = system.select_atoms("name N  and resid " + str(res_index+1))[0]               # 
    
    dihedral_angle_list = []                                                                # Assemble List of Dihedral Angles
    for ts in system.trajectory:                                                            # 
        dihedral_angle_list.append( dihedral_angle(atom_N.position, atom_CA.position, atom_C0.position, atom_N1.position) )
    return dihedral_angle_list                                                              # 
    
def get_omega_angle( system, res_index ):
    ### Selection Syntax to Select Atoms ###                                                ### Selection Syntax to Select Atoms ###
    atom_CA0 = system.select_atoms("name CA and resid " + str(res_index-1))[0]              # 
    atom_C0  = system.select_atoms("name C  and resid " + str(res_index-1))[0]              # 
    atom_N1  = system.select_atoms("name N  and resid " + str(res_index  ))[0]              # 
    atom_CA1 = system.select_atoms("name CA and resid " + str(res_index  ))[0]              # 
    
    
    dihedral_angle_list = []                                                                # Assemble List of Dihedral Angles
    for ts in system.trajectory:                                                            # 
        dihedral_angle_list.append( dihedral_angle(atom_CA0.position, atom_C0.position, atom_N1.position, atom_CA1.position) )
    return dihedral_angle_list                                                              # 

# http://www.ccp14.ac.uk/ccp/web-mirrors/garlic/garlic/commands/dihedrals.html
def get_chi1_angle( system, res_index ):
    ### Selection Syntax to Select Atoms ###                                                ### Selection Syntax to Select Atoms ###
    atom_N  = system.select_atoms("name N  and resid " + str(res_index))[0]                 # 
    atom_CA = system.select_atoms("name CA and resid " + str(res_index))[0]                 # 
    atom_CB = system.select_atoms("name CB and resid " + str(res_index))[0]                 # 
    atom_CG = system.select_atoms("name CG1 and resid " + str(res_index))[0]                 # 
    #if((atom_CB == None) or (atom_CG == None)):
        #return None
    
    dihedral_angle_list = []                                                                # Assemble List of Dihedral Angles
    for ts in system.trajectory:                                                            # 
        dihedral_angle_list.append( dihedral_angle(atom_N.position, atom_CA.position, atom_CB.position, atom_CG.position) )
    return dihedral_angle_list                                                              # 

def list_to_dat(list,path):                     # 
    file = open(path,"w+")                      # 
    for item in list:                           # 
        file.write(str(item)+"\n")                        # 
    file.close()                                # 

def radians_to_degrees(radians):
    degrees = []
    for i in radians:
        degrees.append(i*180/math.pi)
    return degrees


