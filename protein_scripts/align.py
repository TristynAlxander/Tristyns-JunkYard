import MDAnalysis
import numpy as np
from MDAnalysis.analysis import align
if (__name__ == "__main__"):
    import os
    import sys


def centroid(points):                           # Takes a Numpy Matrix
    
    number     = float(points.shape[0])         # number of points
    dimensions = points.shape[1]                # dimension of points
    
    sum = np.zeros(dimensions)                  # Start with zeros
    for point in points:                        # Sum Every Point
        sum = sum + point                       # 
    centroid = sum/float(number)                # Divide by Number of Points
    
    return centroid                             # Return Centroid

def translate(points,vec):
    # Bad Inputs                                                                ### Bad Inputs ###
    if(  vec.size          != 3):                                               # Not 3D Vector
        print("Translate Function Bad Input: Not a 3D Vector.")                 # 
        print("Returning None")                                                 # 
        return None                                                             # 
    elif(len(points.shape) != 2):                                               # Not Point Array Shaped
        print("Translate Function Bad Input: Not an array of points.")          # 
        print("Returning None")                                                 # 
        return None                                                             # 
    elif(points.shape[1]   != 3):                                               # Rows Not Points
        print("Translate Function Bad Input: Rows should be points.")           # 
        print("Returning None")                                                 # 
        return None                                                             # 
    
    
    ### Create Translation Matrix ###                                           ### Create Translation Matrix ###
    partial_translation_matrix = np.matrix([                                    # 
        [1,0,0],                                                                # 1  0  0  dx
        [0,1,0],                                                                # 0  1  0  dy 
        [0,0,1],                                                                # 0  0  1  dz 
        [0,0,0]                                                                 # 0  0  0  1
        ])                                                                      # 
    last_column        = np.vstack(( vec.reshape(3,1) , np.ones((1,1)) ))       # Input Vector is [dx,dy,dz]
    translation_matrix = np.hstack((partial_translation_matrix,last_column))    # 
    #print(translation_matrix)                                                  #
    
    
    ### Create Input Matrix ###                                                 ### Create Input Matrix ### 
    one_column   = np.ones((points.shape[0] ,1))                                # Create Column of Ones
    input_matrix = np.hstack((points,one_column))                               # Add    Column of Ones
    #print(input_matrix.transpose())                                            #
    
    
    ### Translate Points ###                                                    ### Translate Points ###
    product_matrix = np.matmul(translation_matrix, input_matrix.transpose())    # Translate
    output_matrix  = np.delete(product_matrix.transpose(),3,1)                  # Back To Input Format
    #                np.delete( Matrix, Index, Axis)
    
    return output_matrix
"""
def kabsch_algorithm(from_points,to_points):                                                                           # 
    ### Bad Inputs ###                                                          ### Bad Inputs ###
    if(  len(from_points) != len(to_points)):                                   # Not Matching Points 
        print("Kabsch Algorithm Function Bad Input: Not Matching Points .")     # 
        print("Returning None")                                                 # 
        return None                                                             # 
    elif(len(from_points.shape) != 2 or len(to_points.shape) != 2):             # Not Point Array Shaped
        print("Kabsch Algorithm Bad Input: Not an array of points.")            # 
        print("Returning None")                                                 # 
        return None                                                             # 
    elif(from_points.shape[1]   != 3 or to_points.shape[1]   != 3):             # Rows Not Points
        print("Kabsch Algorithm Function Bad Input: Rows should be points.")    # 
        print("Returning None")                                                 # 
        return None                                                             # 
    
    # P = from_points
    # Q = to_points
    # A = covariance_matrix
    covariance_matrix = np.matmul(from_points.transpose(),to_points)
    
    
    #np.matmul(covariance_matrix.transpose(),covariance_matrix)^(1/2)       np.linalg.det(covariance_matrix)
    
    if( np.linalg.det(rotation_matrix) < 0 ): # If this is an improper rotation, Correct it.
        
    
    
    # Singular Value Decomposition 
    # https://cnx.org/contents/HV-RsdwL@23/Molecular-Distance-Measures
"""

# Main                                                                                                      # Main
if __name__ == "__main__":
    points = np.matrix([
        [1,2,3],
        [1,2,5],
        [1,-1,3]
        ])
    
    #n,m = X.shape[0] 
    #n,m = X.shape 
    #one_matrix = np.ones((n,1))
    #Xnew = np.hstack((X,X0))
    
    
    translation_vec   = np.multiply(centroid(points),-1.0)
    
    translated_points = translate(points,translation_vec)
    
    print(centroid(translated_points))
    