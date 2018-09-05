# Import

import numpy as np
import math

# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys


class Atom:
    
    def __init__(self,*args):
        self.atom_type      = "ATOM"    # Str
        self.atom_number    = None      # Unique Int, aside from alt_id
        self.atom_name      = ""        # Str 
        self.element        = ""        # Str
        self.seg_id         = ""        # Str
        self.chain_id       = ""        # char
        self.residue_name   = ""        # Str
        self.residue_number = None      # Int
        self.alt_id         = ""        # char 
        self.insert_code    = ""        # char
        self.occupancy      = 1         # float
        self.temp_factor    = 0         # float
        
        self.x_coordinate   = None      # float
        self.y_coordinate   = None      # float 
        self.z_coordinate   = None      # float
        
        self.is_protein     = None
        self.is_solvent     = None
        self.connects       = []        # TODO: List of Atoms
        self.charge         = None
        self.mass           = None
        
        if( (len(args)==1) and (type(args[0]) is str) ):                            # If given a pdb line
            self.from_pdb_line(args[0])                                             # Convert to Atom
            
    def coordinates(self):
        return [self.x_coordinate, self.y_coordinate, self.z_coordinate]
    
    
    # Converters
    
    ## pdb
    def from_pdb_line(self,line):
        # TODO Note differences if for already filled fields
        # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
        self.atom_type      =       line[ 0:6 ].strip()
        self.atom_number    = int(  line[ 6:11].strip())
        self.atom_name      =       line[12:16].strip()
        self.alt_id         =       line[ 16  ].strip()
        self.residue_name   =       line[17:21].strip().upper()
        self.chain_id       =       line[ 21  ].strip()
        self.residue_number = int(  line[22:26].strip())
        self.insert_code    =       line[ 26  ].strip()
        self.x_coordinate   = float(line[30:38].strip())
        self.y_coordinate   = float(line[38:46].strip())
        self.z_coordinate   = float(line[46:54].strip())
        self.occupancy      = float(line[54:60].strip())
        self.temp_factor    = float(line[60:66].strip())
        self.seg_id         =       line[72:76].strip()
        self.element        =       line[76:78].strip()
    def to_pdb_line(self):
        # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
        line = (
               "{0:<6.6}".format(                 self.atom_type      )
            +    "{0:>5}".format(                 self.atom_number    )
            +  " "                                                  
            +  "{0:>4.4}".format(  "{0:3}".format(self.atom_name    ) )
            +  "{0:<1.1}".format(                 self.alt_id         )
            +  "{0:<4.4}".format( "{0:>3}".format(self.residue_name ) )
            +  "{0:<1.1}".format(                 self.chain_id       )
            +    "{0:>4}".format(                 self.residue_number )
            +  "{0:<1.1}".format(                 self.insert_code    )
            + "   "                                                
            + "{0:>8.3f}".format(                self.x_coordinate    )
            + "{0:>8.3f}".format(                self.y_coordinate    )
            + "{0:>8.3f}".format(                self.z_coordinate    )
            + "{0:>6.2f}".format(                self.occupancy       )
            + "{0:>6.2f}".format(                self.temp_factor     )
            + "      "                                             
            +  "{0:<4.4}".format(                 self.seg_id         )
            +  "{0:>2.2}".format(                 self.element        )
            )
        return line
    def add_pdb_line(self,line):
        print("")# TODO
    
    ## psf
    def from_psf_line(self,line):
        # Divide Line                                                           # No Consistent Division
        fields = line.strip().split()                                           # Divide by White-Space
        
        # atom ID    segment name    residue ID  residue name    atom name   atom type   charge          mass            
        # TODO Note differences if for already filled fields
        self.atom_number    = int(fields[0])
        self.seg_id         = fields[1]
        self.residue_number     = int(fields[2])().upper()
        self.residue_name       = int(fields[2])
        self.atom_name      = None
        self.atom_type      = None
        self.charge         = None
        self.mass           = None
        # 11 = " "
        self.seg_id         = int(  line[ 12:21].strip())
        
        self.atom_number    = int(  line[ 6:11].strip())
        self.atom_name      =       line[12:16].strip()
        self.alt_id         =       line[ 16  ].strip()
        self.residue_name       =       line[17:21].strip().upper()
        self.chain_id       =       line[ 21  ].strip()
        self.residue_number     = int(  line[22:26].strip())
        self.insert_code    =       line[ 26  ].strip()
        self.x_coordinate   = float(line[30:38].strip())
        self.y_coordinate   = float(line[38:46].strip())
        self.z_coordinate   = float(line[46:54].strip())
        self.occupancy      = float(line[54:60].strip())
        self.temp_factor    = float(line[60:66].strip())
        self.seg_id         =       line[72:76].strip()
        self.element        =       line[76:78].strip()
    def to_psf_line(self):
        print("")# TODO
    def add_psf_line(self,line):
        print("")# TODO
    
    # Analysis
    def is_water(self):
        return (self.residue_name == "WAT" or self.residue_name == "HOH" or self.residue_name == "H2O")
    
        
class System:
    
    def __init__(self,*args):
        self.atom_array     = []
        # TODO Add different file types
        
        
        if( (len(args)==1) and (type(args[0]) is str) and (args[0][-4:] == ".pdb")):    # If given a pdb line
            self.load_pdb(args[0])
        
    def select( self, 
                atom_type       = None,
                atom_number     = None,
                atom_name       = None,
                element         = None,
                seg_id          = None,
                chain_id        = None,
                residue_name    = None,
                residue_number  = None,
                alt_id          = None,
                insert_code     = None,
                occupancy       = None,
                temp_factor     = None,
                
                x_coordinate    = None,
                x_high          = None,
                x_low           = None,
                y_coordinate    = None,
                y_high          = None,
                y_low           = None,
                z_coordinate    = None,
                z_high          = None,
                z_low           = None,
                
                is_protein      = None,
                is_solvent      = None,
                connects        = None,
                charge          = None,
                mass            = None
                ):
        atom_list = []
        
        # Repair Chain Input
        if((not chain_id == None) and (not type(chain_id) == list)):
            chain_id = [chain_id]
        
        for a in self.atom_array:
            get_atom    = ( ( ( atom_type      == None ) or ( a.atom_type      == atom_type      ) ) and 
                            ( ( atom_number    == None ) or ( a.atom_number    == atom_number    ) ) and 
                            ( ( atom_name      == None ) or ( a.atom_name      == atom_name      ) ) and 
                            ( ( element        == None ) or ( a.element        == element        ) ) and 
                            ( ( seg_id         == None ) or ( a.seg_id         == seg_id         ) ) and 
                            ( ( chain_id       == None ) or ( a.chain_id       in chain_id       ) ) and 
                            ( ( residue_name   == None ) or ( a.residue_name   == residue_name   ) ) and 
                            ( ( residue_number == None ) or ( a.residue_number == residue_number ) ) and 
                            ( ( alt_id         == None ) or ( a.alt_id         == alt_id         ) ) and 
                            ( ( insert_code    == None ) or ( a.insert_code    == insert_code    ) ) and 
                            ( ( occupancy      == None ) or ( a.occupancy      == occupancy      ) ) and 
                            ( ( temp_factor    == None ) or ( a.temp_factor    == temp_factor    ) ) and 
                            # Coordinate Conditions
                            ( ( x_coordinate   == None ) or ( a.x_coordinate   == x_coordinate   ) ) and 
                            ( ( x_high         == None ) or ( a.x_high         <  x_high         ) ) and 
                            ( ( x_low          == None ) or ( a.x_low          >  x_low          ) ) and 
                            ( ( y_coordinate   == None ) or ( a.y_coordinate   == y_coordinate   ) ) and 
                            ( ( y_high         == None ) or ( a.y_high         <  y_high         ) ) and 
                            ( ( y_low          == None ) or ( a.y_low          >  y_low          ) ) and 
                            ( ( z_coordinate   == None ) or ( a.z_coordinate   == z_coordinate   ) ) and 
                            ( ( z_high         == None ) or ( a.z_high         <  z_high         ) ) and 
                            ( ( z_low          == None ) or ( a.z_low          >  z_low          ) ) and 
                            
                            ( ( is_protein     == None ) or ( a.is_protein     == is_protein     ) ) and 
                            ( ( is_solvent     == None ) or ( a.is_solvent     == is_solvent     ) ) and 
                            ( ( connects       == None ) or ( a.connects       == connects       ) ) and 
                            ( ( charge         == None ) or ( a.charge         == charge         ) ) and 
                            ( ( mass           == None ) or ( a.mass           == mass           ) ) )
            # Add-to-List
            if(get_atom):
                atom_list.append(a)
        return atom_list
    
    # System Analysis
    def __radians_to_degrees__(radians):
        degrees = []
        for i in radians:
            degrees.append(i*180/math.pi)
        return degrees
    def __list_to_dat__(list,path):                 # 
        file = open(path,"w+")                      # 
        for item in list:                           # ToDo: make sure is white space delimited if Matrix
            file.write(str(item)+"\n")              # 
        file.close()                                # 

        
    ## Bond Lengths by Dihedrals
    def distance(atom1,atom2):
        vec1   = np.array(atom1.coordinates())
        vec2   = np.array(atom2.coordinates())
        length = np.linalg.norm(np.subtract(vec1,vec2))
        return length
    
    def distance_backbone_phi(self, residue_index,chain_id):
        s1 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )         #
        if( s1==[] or s2==[] ):                                                                         # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 ):                                                              #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.distance(s1[0],s2[0])                                                         # Return Distance
    
    def distance_backbone_psi(self, residue_index,chain_id):
        s1 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="C"  , residue_number=residue_index   , chain_id=chain_id )         #
        if( s1==[] or s2==[] ):                                                                         # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 ):                                                              #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.distance(s1[0],s2[0])                                                         # Return Distance
            
    def distance_backbone_omega(self, residue_index,chain_id):
        s1 = self.select( atom_name="C"  , residue_number=residue_index-1 , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )         #
        if( s1==[] or s2==[] ):                                                                         # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 ):                                                              #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.distance(s1[0],s2[0])                                                         # Return Distance
    
    
    ## Angles by Backbone
    def angle(atom1,atom2,atom3):
        a1 = np.array(atom1.coordinates())                              # Get Atom Coordinates
        a2 = np.array(atom2.coordinates())                              #
        a3 = np.array(atom3.coordinates())                              #
        
        v1 = np.subtract(a1,a2.transpose())                             # Convert to Vectors
        v2 = np.subtract(a3,a2.transpose())                             #
        
        v1_norm = np.linalg.norm(v1)                                    # Get Vector Normals
        v2_norm = np.linalg.norm(v2)                                    # 
        
        return math.acos(float(np.dot(v1,v2))/float(v1_norm*v2_norm))   # Solve for Angle using Dot Product Cosine Equation 
       
    def angle_backbone_n(     self, residue_index, chain_id ):
        s1 = self.select( atom_name="C"  , residue_number=residue_index-1 , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )         #
        s3 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )         #
        if( s1==[] or s2==[] or s3==[] ):                                                               # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 ):                                                 #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.angle(s1[0],s2[0],s3[0])                                                      # Return Angle
        
    def backbone_angle_ca(    self, residue_index, chain_id ):
        s1 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )         #
        s3 = self.select( atom_name="C"  , residue_number=residue_index   , chain_id=chain_id )         #
        if( s1==[] or s2==[] or s3==[] ):                                                               # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 ):                                                 #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.angle(s1[0],s2[0],s3[0])                                                      # Return Angle
        
    def backbone_angle_co(    self, residue_index, chain_id ):
        s1 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )         # Selection
        s2 = self.select( atom_name="C"  , residue_number=residue_index   , chain_id=chain_id )         #
        s3 = self.select( atom_name="N"  , residue_number=residue_index+1 , chain_id=chain_id )         #
        if( s1==[] or s2==[] or s3==[] ):                                                               # Verify Selection
            return None                                                                                 #
        else:                                                                                           #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 ):                                                 #
                print("Warning: Non-Unique Selection, Using First.")                                    #
            return System.angle(s1[0],s2[0],s3[0])                                                      # Return Angle
        
        
    
    ## Dihedrals
    def __vector_projection__(a,b,debug=False):
        # Vector Projection Equation:
        #   \text{proj}_{\vec{b}} \vec{a}  = \frac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2} \vec{b}
        
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
    
    def __plane_projection__(a,normal,debug=False):
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
        return np.subtract(a,System.__vector_projection__(a,normal))
    
    def __dihedral_angle__(a,b,c,d,debug=False):
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
        
        if(debug):
            if(not (type(a) is list or type(a) is np.matrix)):                                      # Verify vector A is list or matrix
                return None                                                                         # 
            elif(not (type(b) is list or type(b) is np.matrix)):                                    # Verify vector B is list or matrix
                return None                                                                         # 
            elif(not (type(c) is list or type(c) is np.matrix)):                                    # Verify vector B is list or matrix
                return None                                                                         # 
            elif(not (type(d) is list or type(d) is np.matrix)):                                    # Verify vector B is list or matrix
                return None                                                                         # 
            else:
                if(type(a) is list):                                                                # Make Lists into Matrix
                    a = np.matrix(a)                                                                # 
                if(type(b) is list):                                                                # 
                    b = np.matrix(b)                                                                # 
                if(type(c) is list):                                                                # 
                    c = np.matrix(c)                                                                # 
                if(type(d) is list):                                                                # 
                    d = np.matrix(d)                                                                # 
                
                if(a.size != 3):                                                                    # Verify Vectors are a reasonable size
                    print("Need a 3D vector, not size: "+str(a.size) )                              # 
                    return None                                                                     # 
                if(b.size != 3):                                                                    # Verify Vectors are a reasonable size
                    print("Need a 3D vector, not size: "+str(b.size) )                              # 
                    return None                                                                     # 
                if(c.size != 3):                                                                    # Verify Vectors are a reasonable size
                    print("Need a 3D vector, not size: "+str(c.size) )                              # 
                    return None                                                                     # 
                if(d.size != 3):                                                                    # Verify Vectors are a reasonable size
                    print("Need a 3D vector, not size: "+str(d.size) )                              # 
                    return None                                                                     # 
                
                if( (len(a.shape) != 2) or (not 1 in a.shape)):                                     # Verify Vectors have useful shape
                    print("Vector Projection: First Vector has improper shape: " +str(a.shape))     # 
                    return None                                                                     # 
                if( (len(b.shape) != 2) or (not 1 in b.shape)):                                     # 
                    print("Vector Projection: Second Vector has improper shape: "+str(b.shape))     # 
                    return None                                                                     # 
                if( (len(c.shape) != 2) or (not 1 in c.shape)):                                     # 
                    print("Vector Projection: Third Vector has improper shape: "+str(c.shape))      # 
                    return None                                                                     # 
                if( (len(d.shape) != 2) or (not 1 in d.shape)):                                     # 
                    print("Vector Projection: Fourth Vector has improper shape: "+str(d.shape))     # 
                    return None                                                                     #
                
                if(a.shape[0] != 1):                                                                # Correct Transposed Shapes
                    a = a.transpose()                                                               #
                if(b.shape[0] != 1):                                                                # 
                    b = b.transpose()                                                               # 
                if(c.shape[0] != 1):                                                                # 
                    c = c.transpose()                                                               # 
                if(d.shape[0] != 1):                                                                # 
                    d = d.transpose()                                                               # 
        
        b_to_a            = np.subtract(b,a)                                            # Get Appropriate Vectors
        b_to_c            = np.subtract(b,c)                                            # 
        c_to_b            = np.subtract(c,b)                                            # 
        c_to_d            = np.subtract(c,d)                                            # 
        
        perpendicular     = c_to_b                                                      # TODO: Is this the right perpendicular? c_to_b
        
        unit_normal       = np.dot(perpendicular , 1/np.linalg.norm(perpendicular) )    # Unit Normal, to make everything a scale properly.
        
        front_projection  = System.__plane_projection__( b_to_a , unit_normal )                # Front & Back Projections
        back_projection   = System.__plane_projection__( c_to_d , unit_normal )                # See Diagram above. 
        
        cross_product    = np.cross(front_projection,back_projection)                   # Sine component of the determinant
        determinant      = np.dot(unit_normal,cross_product.transpose())                # Determinant is proportional to sine
        dot_product      = np.dot(front_projection,back_projection.transpose())         # Dot-Product is proportional to cosine
        
        theta = math.atan2(determinant, dot_product)                                    # Get Angle
        
        return theta
        
    def atom_dihedral( atom1, atom2, atom3, atom4):
        a = np.matrix( atom1.coordinates() )
        b = np.matrix( atom2.coordinates() )
        c = np.matrix( atom3.coordinates() )
        d = np.matrix( atom4.coordinates() )
        return System.__dihedral_angle__(a,b,c,d)
    
    # http://www.ccp14.ac.uk/ccp/web-mirrors/garlic/garlic/commands/dihedrals.html
    
    def dihedral_phi(self, residue_index, chain_id):
        s1 = self.select( atom_name="C"  , residue_number=residue_index-1 , chain_id=chain_id )     # Selection
        s2 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )     #
        s3 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )     #
        s4 = self.select( atom_name="C"  , residue_number=residue_index   , chain_id=chain_id )     #
        if( s1==[] or s2==[] or s3==[] or s4==[] ):                                                 # Verify Selection
            return None                                                                             #
        else:                                                                                       #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 or len(s4)>1):                                 #
                print("Warning: Non-Unique Selection, Using First.")                                #
            return System.atom_dihedral(s1[0],s2[0],s3[0],s4[0])                                    # Return Dihedral
        
    def dihedral_psi(self, residue_index, chain_id):
        s1 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )     # Selection
        s2 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )     #
        s3 = self.select( atom_name="C"  , residue_number=residue_index   , chain_id=chain_id )     #
        s4 = self.select( atom_name="N"  , residue_number=residue_index+1 , chain_id=chain_id )     #
        if( s1==[] or s2==[] or s3==[] or s4==[] ):                                                 # Verify Selection
            return None                                                                             #
        else:                                                                                       #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 or len(s4)>1):                                 #
                print("Warning: Non-Unique Selection, Using First.")                                #
            return System.atom_dihedral(s1[0],s2[0],s3[0],s4[0])                                    # Return Dihedral
    
    def dihedral_omega(self, residue_index, chain_id):
        s1 = self.select( atom_name="CA" , residue_number=residue_index-1 , chain_id=chain_id )     # Selection
        s2 = self.select( atom_name="C"  , residue_number=residue_index-1 , chain_id=chain_id )     #
        s3 = self.select( atom_name="N"  , residue_number=residue_index   , chain_id=chain_id )     #
        s4 = self.select( atom_name="CA" , residue_number=residue_index   , chain_id=chain_id )     #
        if( s1==[] or s2==[] or s3==[] or s4==[] ):                                                 # Verify Selection
            return None                                                                             #
        else:                                                                                       #
            if( len(s1)>1 or  len(s2)>1 or len(s3)>1 or len(s4)>1):                                 #
                print("Warning: Non-Unique Selection, Using First.")                                #
            return System.atom_dihedral(s1[0],s2[0],s3[0],s4[0])                                    # Return Dihedral
        
    
    def get_residue(self, residue_index, chain_id):
        s1 = self.select( atom_name="CA" , residue_number=residue_index , chain_id=chain_id )       # Selection
        if( s1==[] ):                                                                               # Verify Selection
            return None                                                                             #
        else:                                                                                       #
            if( len(s1)>1 ):                                                                        #
                print("Warning: Non-Unique Selection, Using First.")                                #
            return s1[0].residue_name                                                               # Return Dihedral
    
    def residue_count(self, chain_id):
        # Initial States                                                                                    # Initial States
        residue_count       = 0                                                                             #   Initial Residue Count
        last_residue_name   = ""                                                                            #   No Initial Residue
        last_residue_number = ""                                                                            #   No Initial Number
        for atom in self.atom_array:                                                                        # Loop
            if(atom.chain_id == chain_id):                                                                  # Limit Interest
                # Detect Residue Changes                                                                    # Detect Residue Changes
                new_residue_name    = atom.residue_name                           != last_residue_name      #   Name Changes
                new_residue_number  = (str(atom.residue_number)+atom.insert_code) != last_residue_number    #   Number or Insertion Code Changes
                residue_change      = new_residue_name or new_residue_number                                #   Either Change
                # Increment Count                                                                           # Increment Count
                if(residue_change):                                                                         #
                    residue_count = residue_count + 1                                                       #
                # Store Residue                                                                             # Store Residue
                last_residue_name   = atom.residue_name                                                     #   Residue Name
                last_residue_number = (str(atom.residue_number)+atom.insert_code)                           #   Residue Number & Insertion Code
                last_chain          = atom.chain_id                                                         #   Chain
        return residue_count                                                                                # Return Count
    
    # Modify System 
    def renumber_atoms(self):
        atom_num = 0
        for atom in self.atom_array:
            atom_num = atom_num + 1
            atom.atom_number = atom_num
    
    
    def renumber_residues(self):
        self.renumber_residues_by_chain()
    
    def renumber_residues_by_chain(self):
        # Initial States                                                                                # Initial States
        residue_number      = 0                                                                         #   Initial Residue Number
        last_residue_name   = ""                                                                        #   No Initial Residue
        last_residue_number = ""                                                                        #   No Initial Number
        last_chain          = ""                                                                        #   No Initial Chain
        for atom in self.atom_array:                                                                    # 
            # Detect Changes                                                                            # Detect Change
            chain_change  = last_chain != atom.chain_id                                                 #   Chain Changes
            new_residue_name    = atom.residue_name != last_residue_name                                #   Residue Name Changes
            new_residue_number  = (str(atom.residue_number)+atom.insert_code) != last_residue_number    #   Residue Number & Insertion Code Changes
            residue_change      = new_residue_name or new_residue_number or chain_change                #   Any Change
            # Store Last State                                                                          # Store Last State
            last_chain          = atom.chain_id                                                         #   Chain
            last_residue_name   = atom.residue_name                                                     #   Residue Name
            last_residue_number = (str(atom.residue_number)+atom.insert_code)                           #   Residue Number & Insertion Code
            # Reset Residue Number                                                                      # Reset Residue Number
            if(chain_change):                                                                           #
                residue_number = 0                                                                      #
            # Renumber Residues                                                                         # Renumber Residues
            if(residue_change):                                                                         #   If Residue Changed
                residue_number = residue_number + 1                                                     #   Increment residue_number
            atom.residue_number = residue_number                                                        # Set Residue Number
            atom.insert_code = ""                                                                       # Strip Insertion Codes
            
    def renumber_residues_all(self):
        # Initial State                                                                                 # Initial State
        residue_number      = 0                                                                         # Initial Residue Number
        last_residue_name   = ""                                                                        # No Initial Residue
        last_residue_number = ""                                                                        # No Initial Number
        for atom in self.atom_array:                                                                    # 
            # Detect Changes                                                                            # Detect Changes
            new_residue_name    = atom.residue_name != last_residue_name                                #   Name Changes
            new_residue_number     = (str(atom.residue_number)+atom.insert_code) != last_residue_number #   Number & Insertion Code Changes
            residue_change      = new_residue_name or new_residue_number                                #   Any Change
            # Store Last State                                                                          # Store Last State
            last_residue_name   = atom.residue_name                                                     #   Residue Name
            last_residue_number = (str(atom.residue_number)+atom.insert_code)                           #   Residue Number & Insertion Code
            # Renumber Residues                                                                         # Renumber Residues
            if(residue_change):                                                                         #   If Residue Changed
                residue_number = residue_number + 1                                                     #   Increment residue_number
            atom.residue_number = residue_number                                                        # Set Residue Number
            atom.insert_code = ""                                                                       # Strip Insertion Codes
            
    def reseq_chain(self):
        # Initialize Chain Variables                                    # Initialize Chain Variables
        last_chain      = ""                                            # No Initial Chain
        chain_num       = -1                                            # Start Number - 1 = -1
        ALPHABET = [chr(ascii) for ascii in range(65, 91)]              # Alphabet List
        for atom in self.atom_array:                                    #
            chain_change  = last_chain != atom.chain_id                 # Detect Chain Change
            last_chain    = atom.chain_id                               # Store Chain
            if(chain_change):                                           # 
                chain_num = chain_num + 1                               # Increment Chain
            atom.chain_id = ALPHABET[chain_num]                         # Set Chain
            
    def check(self):
        print("")
        # TODO Add Check non-solvent molecules have chains
        # TODO Check Resid is continuous
    def add_system(self,system):
        print("Incomplete")
        # Will Combine Systems.
    
    def strip_water(self):
        self.atom_array[:] = [x for x in self.atom_array if not x.is_water()]
        
    # pdb
    def load_pdb(self,pdb_path):                                                    # Load (Initial) PDB File
        # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
        
        if(len(self.atom_array) != 0):                                              # Check Empty System
            print("Warning (load_pdb): Overriding Existing System.")                # Warn User
            self.atom_array = []                                                    # Overwrite System.
        
        pdb_file = open(pdb_path)                                                   # Get  PDB  File
        
        for line in pdb_file:                                                       # Horizontal Split ( into rows    ) 
            fields = line.strip().split()                                           # Vertical   Split ( into columns )
            
            if(fields[0] == "ATOM" or fields[0] == "HETATM"):                       # Narrow Scope: Atoms.
                self.atom_array.append(Atom(line))                                  # Load Atoms
            # TODO Add Defaults
            # TODO Add Connects
            # TODO Define Protein, Solvent, etc
        
        # TODO Resequence  
        print("Incomplete Function Used: load_pdb")   # TODO
    def print_pdb(self,pdb_path):
        pdb_new = open(pdb_path,"w+",newline='')                     # Make new PDB File
        for atom in self.atom_array:
            # ToDo: Check if need to insert Terminal
            line = atom.to_pdb_line()
            pdb_new.write(line+"\n")
        pdb_new.write("END")
        pdb_new.close()
    
    # psf
    def load_psf(self,psf_path):
        
        is_new_system   = None
        is_atom_field   = False
        psf_file        = open(psf_path)                                            # Get  PSF  File
        
        for line in psf_file:                                                       # Horizontal Split ( into rows    ) 
            fields = line.strip().split()                                           # Vertical   Split ( into columns )
            
            if(len(fields) >= 2 and fields[1] == "!NATOM"):                         # Find Atom List
                psf_atom_count  = int(fields[0])                                    # Get psf  Atom Count
                self_atom_count = len(self.atom_array)                              # Get self Atom Count
                if(psf_atom_count == self_atom_count):                              # Use Same System
                    is_new_system = False                                           # 
                    print("Notice (load_psf): Same Atom Count")                     # 
                    print("Notice (load_psf): Combining Files")                     # 
                else:                                                               # Use New System
                    is_new_system = True                                            # 
                    print("Warning (load_psf): Different Atom Count")               # 
                    print("Warning (load_psf): Overriding Existing System")         # 
                    self.atom_array = []                                            # 
            
        print("Incomplete Function.")   # TODO
    # PSF Files: atoms, bonds, angles, dihedrals, impropers
    #atom ID    segment name    residue ID  residue name    atom name   atom type   charge          mass            
    #1          PROA            25          GLU             N           NH3         -0.300000       14.0070           0   0.00000     -0.301140E-02
    #       3   SEG             25          GLU             HT2         HC          0.330000        1.0080              0

    # PSF Formats: CHARMM or X-PLOR
    # Charmm uses numbers instead of atom_type
    # Most things require atom order match exactly to pdb, so safe-ish assumption.
    #

# Tools for Processing PDB Files.
# 
# PDB Format Functions (below) via: 

# Mostly followed that, mostly.
#
# ATOM
#1-4    "ATOM"                                  character   "{0:<4}  "
#6-11   Atom Serial Number              right   integer     "{0:>6} "
#13-16  Atom Name                       left*   character   " {0:<3}"
#17     Alternate Location Indicator            character   "{0:<1}"
#18-20  Residue Name                    right   character   "{0:>3} "
#22     Chain Identifier                        character   "{0:<1}"
#23-26  Residue Sequence Number         right   integer     "{0:>4}"
#27     Insertion Codes of Residues             character   "{0:<1}   "
#31-38  X Orthogonal A Coordinate       right   real        "{0:>8}"
#39-46  Y Orthogonal A Coordinate       right   real        "{0:>8}"
#47-54  Z Orthogonal A Coordinate       right   real        "{0:>8}"
#55-60  Occupancy                       right   real        "{0:>6}"
#61-66  Temperature Factor              right   real        "{0:>6}      "
#73-76  Segment Identifier              left    character   "{0:>4}"
#77-78  Element Symbol                  right   character   "{0:>2}"
#
# TER
#1-3    "TER"                                   character   "{0:<3}   "
#7-11   Serial Number                   right   integer     "{0:>5}      "
#18-20  Residue Name                    right   character   "{0:>3} "
#22     Chain Identifier                        character   "{0:<1}"
#23-26  Residue Sequence Number         right   integer     "{0:>4}"
#27     Insertion Codes of Residues             character   "{0:<1}"
#
# ATOM
def line_to_pdb_atom(line):
    fields = []
    fields.append(line[0:6].strip())                # 0  str    ATOM
    fields.append(int(line[6:11].strip()))          # 1  int    Atom Serial Number
    fields.append(line[12:16].strip())              # 2  str    Atom Name
    fields.append(line[16].strip())                 # 3  str    Alternate Location Indicator
    fields.append(line[17:21].strip())              # 4  str    Residue Name
    fields.append(line[21].strip())                 # 5  str    Chain Identifier
    fields.append(int(line[22:26].strip()))         # 6  int    Residue Sequence Number
    fields.append(line[26].strip())                 # 7  str    Insertion Codes of Residues
    fields.append(float(line[30:38].strip()))       # 8  float  X Orthogonal A Coordinate
    fields.append(float(line[38:46].strip()))       # 9  float  Y Orthogonal A Coordinate
    fields.append(float(line[46:54].strip()))       # 10 float  Z Orthogonal A Coordinate
    fields.append(float(line[54:60].strip()))       # 11 float  Occupancy
    fields.append(float(line[60:66].strip()))       # 12 float  Temperature Factor
    fields.append(line[72:76].strip())              # 13 str    Segment Identifier
    fields.append(line[76:78].strip())              # 14 str    Element Symbol
    return fields
def print_atom_fields(fields):
    print("{0:<30.30}{1}".format("ATOM: "               , fields[0].replace(" ","_")))        # 0  ATOM
    print("{0:<30.30}{1}".format("Atom Number: "        , str(fields[1]).replace(" ","_")))        # 1  Atom Serial Number
    print("{0:<30.30}{1}".format("Atom Name: "          , fields[2].replace(" ","_")))        # 2  Atom Name
    print("{0:<30.30}{1}".format("Alt Location: "       , fields[3].replace(" ","_")))        # 3  Alternate Location Indicator
    print("{0:<30.30}{1}".format("Residue Name: "       , fields[4].replace(" ","_")))        # 4  Residue Name
    print("{0:<30.30}{1}".format("Chain Id: "           , fields[5].replace(" ","_")))        # 5  Chain Identifier
    print("{0:<30.30}{1}".format("Res Number: "         , str(fields[6]).replace(" ","_")))        # 6  Residue Sequence Number
    print("{0:<30.30}{1}".format("Insertion Code: "     , fields[7].replace(" ","_")))        # 7  Insertion Codes of Residues
    print("{0:<30.30}{1}".format("X Coordinate: "       , str(fields[8])))        # 8  X Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Y Coordinate: "       , str(fields[9])))        # 9  Y Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Z Coordinate: "       , str(fields[10])))       # 10 Z Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Occupancy: "          , str(fields[11])))       # 11 Occupancy
    print("{0:<30.30}{1}".format("Temperature Factor: " , str(fields[12])))       # 12 Temperature Factor
    print("{0:<30.30}{1}".format("Seg Id: "             , fields[13].replace(" ","_")))       # 13 Segment Identifier
    print("{0:<30.30}{1}".format("Element: "            , fields[14].replace(" ","_")))       # 14 Element Symbol

def pdb_atom_to_line(fields):
    # Check Types
    atom_type    = fields[0]
    atom_number  = fields[1]
    atom_name    = fields[2]
    alt_id       = fields[3]
    residue_name     = fields[4]
    chain_id     = fields[5]
    residue_number   = fields[6]
    insert_code  = fields[7]
    x_coordinate = fields[8]
    y_coordinate = fields[9]
    z_coordinate = fields[10]
    occupancy    = fields[11]
    temp_factor  = fields[12]
    seg_id       = fields[13]
    element      = fields[14]
    
    bad_type = False
    if(   not type(fields[0])  is str ):                                    # 0  str    ATOM
        bad_type = True                                                     #
        print("Warning Bad Type: Identifier should be string = \"ATOM\"")   #
    elif( not type(fields[1])  is int ):                                    # 1  int    Atom Serial Number
        bad_type = True                                                     #
        print("Warning Bad Type: Atom Number should be int")                #
    elif( not type(fields[2])  is str ):                                    # 2  str    Atom Name
        bad_type = True                                                     #
        print("Warning Bad Type: Atom Name should be str")                  #
    elif( not type(fields[3])  is str ):                                    # 3  str    Alternate Location Indicator
        bad_type = True                                                     #
        print("Warning Bad Type: Alt Location Indicator should be str")     #
    elif( not type(fields[4])  is str ):                                    # 4  str    Residue Name
        bad_type = True                                                     #
        print("Warning Bad Type: Residue Name should be str")               #
    elif( not type(fields[5])  is str ):                                    # 5  str    Chain Identifier
        bad_type = True                                                     #
        print("Warning Bad Type: Chain Identifier should be str")           #
    elif( not type(fields[6])  is int ):                                    # 6  int    Residue Sequence Number
        bad_type = True                                                     #
        print("Warning Bad Type: Residue Sequence Number should be int")    #
    elif( not type(fields[7])  is str ):                                    # 7  str    Insertion Codes of Residues
        bad_type = True                                                     #
        print("Warning Bad Type: Insertion Code should be str")             #
    elif( not type(fields[8])  is float ):                                  # 8  float  X Orthogonal A Coordinate
        bad_type = True                                                     #
        print("Warning Bad Type: x coordinate should be float")             #
    elif( not type(fields[9])  is float ):                                  # 9  float  Y Orthogonal A Coordinate
        bad_type = True                                                     #
        print("Warning Bad Type: y coordinate should be float")             #
    elif( not type(fields[10]) is float ):                                  # 10 float  Z Orthogonal A Coordinate
        bad_type = True                                                     #
        print("Warning Bad Type: z coordinate should be float")             #
    elif( not type(fields[11]) is float ):                                  # 11 float  Occupancy
        bad_type = True                                                     #
        print("Warning Bad Type: Occupancy should be float")                #
    elif( not type(fields[12]) is float ):                                  # 12 float  Temperature Factor
        bad_type = True                                                     #
        print("Warning Bad Type: Temperature Factor should be float")       #
    elif( not type(fields[13]) is str ):                                    # 13 str    Segment Identifier
        bad_type = True                                                     #
        print("Warning Bad Type: Segment ID should be str")                 #
    elif( not type(fields[14]) is str ):                                    # 14 str    Element Symbol
        bad_type = True                                                     #
        print("Warning Bad Type: Element Symbol should be str")             #
    
    # Convert to String
    line = (
              "{0:<6.6}".format(                atom_type    )
            +   "{0:>5}".format(                atom_number  )
            + " "                                                  
            + "{0:>4.4}".format("{0:3}".format( atom_name  ) )
            + "{0:<1.1}".format(                alt_id       )
            + "{0:<4.4}".format("{0:>3}".format( residue_name   ) )
            + "{0:<1.1}".format(                chain_id     )
            +   "{0:>4}".format(                residue_number   )
            + "{0:<1.1}".format(                insert_code  )
            + "   "                                                
            + "{0:>8.3f}".format(               x_coordinate )
            + "{0:>8.3f}".format(               y_coordinate )
            + "{0:>8.3f}".format(               z_coordinate )
            + "{0:>6.2f}".format(               occupancy    )
            + "{0:>6.2f}".format(               temp_factor  )
            + "      "                                             
            + "{0:<4.4}".format(                seg_id       )
            + "{0:>2.2}".format(                element      )
            )
    return line
# TER
def line_to_pdb_ter(line):
    fields = []
    fields.append(line[0:3].strip())             # 0  TER
    fields.append(int(line[6:11].strip()))       # 1  Atom Serial Number
    fields.append(line[17:20].strip())           # 2  Residue Name
    fields.append(line[21].strip())              # 3  Chain Identifier
    fields.append(int(line[22:26].strip()))      # 4  Residue Sequence Number
    fields.append(line[26].strip())              # 5  Insertion Codes of Residues
    return fields
def pdb_ter_to_line(fields):
    line = (
         "{0:<3.3}   ".format(fields[0])      # 0  ATOM
        +"{0:>5}      ".format(fields[1])     # 1  Atom Serial Number
        +"{0:>3.3} ".format(fields[2])        # 2  Residue Name
        +"{0:<1.1}".format(fields[3])         # 3  Chain Identifier
        +"{0:>4}".format(fields[4])           # 4  Residue Sequence Number
        +"{0:<1.1}   ".format(fields[5])      # 5  Insertion Codes of Residues
        )
    return line

if __name__ == "__main__":
    print("Testing...\n")
    x = System("4ncu.pdb")
    
    x.strip_water()
    x.renumber_atoms()
    x.renumber_residues()
    x.reseq_chain()
    #x.print_pdb("new.pdb")
    
    path = "table.dat"
    file = open(path,"w+")
    
    title_line = "{0:<9.9}{1:<9.9}{2:<9.9}{3:<9.9}{4:<9.9}{5:<9.9}{6:<9.9}{7:<9.9}{8:<9.9}{9:<9.9}{10:<9.9}\n".format( "chain", "residue", "C-N","N-Ca","Ca-C", "<N","<Ca","<C", "omega","phi","psi")
    file.write(title_line)
    
    phi_list = []
    psi_list = []
    res_list = []
    
    # Iterate over Alphabet                                         # Iterate over Alphabet 
    for ascii in range(65, 91):                                     # Iterate over Ascii Uppercase 
        letter = chr(ascii)
        
        for residue_number in range(1,x.residue_count(letter)):
            
            # Bond Lengths
            n_to_ca = x.distance_backbone_phi(     residue_number, letter)
            ca_to_c = x.distance_backbone_psi(    residue_number, letter)
            c_to_n  = x.distance_backbone_omega(     residue_number, letter)
            
            if(n_to_ca == None):
                n_to_ca = "None"
            else:
                n_to_ca = round(n_to_ca,3)
            if(ca_to_c == None):
                ca_to_c = "None"
            else:
                ca_to_c = round(ca_to_c,3)
            if(c_to_n == None):
                c_to_n = "None"
            else:
                c_to_n = round(c_to_n,3)
            
            
            # Angles
            angle_n  = x.angle_backbone_n(  residue_number, letter )
            angle_ca = x.backbone_angle_ca( residue_number, letter )
            angle_co = x.backbone_angle_co( residue_number, letter )
            
            if(angle_n == None):
                angle_n = "None"
            else:
                angle_n = round(angle_n,3)
            if(angle_ca == None):
                angle_ca = "None"
            else:
                angle_ca = round(angle_ca,3)
            if(angle_co == None):
                angle_co = "None"
            else:
                angle_co = round(angle_co,3)
            
            
            # Dihedrals
            phi = x.dihedral_phi(   residue_number, letter )
            psi = x.dihedral_psi(   residue_number, letter )
            omg = x.dihedral_omega( residue_number, letter )
            
            if(phi == None):
                phi = "None"
            else:
                phi = round(phi,3)
            if(psi == None):
                psi = "None"
            else:
                psi = round(psi,3)
            if(omg == None):
                omg = "None"
            else:
                omg = round(omg,3)
            
            phi_list.append(phi)
            psi_list.append(psi)
            res_list.append(x.get_residue(residue_number, letter))
            
            line = "{0:<9.9}{1:<9}{2:<9.9}{3:<9.9}{4:<9.9}{5:<9.9}{6:<9.9}{7:<9.9}{8:<9.9}{9:<9.9}{10:<9.9}\n".format( letter, residue_number, c_to_n, n_to_ca, ca_to_c, angle_n, angle_ca, angle_co, omg, phi, psi)
            file.write(line)
            
    file.close()  
    System.__list_to_dat__(phi_list,"phi.dat")
    System.__list_to_dat__(psi_list,"psi.dat")
    System.__list_to_dat__(res_list,"res.dat")
    