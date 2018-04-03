# Imports
#import pars_pdb
import MDAnalysis
import numpy as np
import math

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys

def dihedral_angle(a,b,c,d):
    
    # <ABC                                      # Difference between two points to form a vector in the plane
    b_to_a         = np.subtract(b,a)           # Vector from b to a
    b_to_c         = np.subtract(b,c)           # Vector from b to c
    abc_norm_vec   = np.cross(b_to_a,b_to_c)    # Normal Vector to the plane
    
    # <BCD                                      # Difference between two points to form a vector in the plane
    c_to_b         = np.subtract(c,b)           # Vector from c to b
    c_to_d         = np.subtract(c,d)           # Vector from c to d
    bcd_norm_vec   = np.cross(c_to_b,c_to_d)    # Normal Vector to the plane
    
    # Dihedral Angle                            # Angel between two planes equals angle between their normal vectors
    #   \[ \vec{v} \cdot \vec{u} = |\vec{v}| |\vec{u}| \cos( \theta ) \]
    #   \[ \theta = \arccos \left( \frac{\vec{v} \cdot \vec{u}}{|\vec{v}| |\vec{u}|}   \right ) \]
    dihedral_angle = np.arccos(np.dot(bcd_norm_vec,abc_norm_vec)/(np.linalg.norm(bcd_norm_vec)*np.linalg.norm(abc_norm_vec)))
    return dihedral_angle

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

def angle(angle,res_index, psf, *traj):                         # 
    if(len(traj) == 1):                                         # Single Point 
        return angle(psf,traj[0],res_index)[-1]                 #   Return Last Frame
    else:                                                       # Multiple
        angle_list = angle(psf,traj[0],res_index)[-1]           #   Last Frame of First Trajectory
        next(traj)                                              #   Skip First Trajectory
        for t in traj:                                          #   
            angle_list = angle_list + angle(psf,t,res_index)    #   Sum Trajectories
        return angle_list                                       #   



# Main                                                                                                      # Main
if __name__ == "__main__":
    
    system    = MDAnalysis.Universe("prod_out_new.pdb","prod_out_new.dcd")                                               # Define System Universe
    
    
    
    
    phi_angle_list = get_phi_angle(system,93)
    degrees_phi_angle_list = radians_to_degrees(phi_angle_list)
    list_to_dat(degrees_phi_angle_list,"Trp_ab_phi_3.dat")
    
    
    chi1_angle_list = get_chi1_angle(system,93)
    degrees_chi1_angle_list = radians_to_degrees(chi1_angle_list)
    list_to_dat(degrees_chi1_angle_list,"Trp_ab_chi1_3.dat")
    
