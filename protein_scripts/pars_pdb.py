
class Atom:
    
    def __init__(self):
        # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
        self.atom_type      = "ATOM"    # Str
        self.atom_number    = None      # Unique Int, aside from alt_id
        self.atom_name      = ""        # Str 
        self.element        = ""        # Str
        self.seg_id         = ""        # Str
        self.chain_id       = ""        # char
        self.res_name       = ""        # Str
        self.res_number     = None      # Int
        self.alt_id         = ""        # char 
        self.insert_code    = ""        # char
        self.occupancy      = 1         # float
        self.temp_factor    = 0         # float
        
        self.x_coordinate   = None      # float
        self.y_coordinate   = None      # float 
        self.z_coordinate   = None      # float
        
        self.is_protein     = None
        self.connects       = []        # Array of Atom_number
        self.charge         = None
        
    def load_pdb_line(self,line):
        self.atom_type      =       line[ 0:6 ].strip()
        self.atom_number    = int(  line[ 6:11].strip())
        self.atom_name      =       line[12:16].strip()
        self.alt_id         =       line[ 16  ].strip()
        self.res_name       =       line[17:21].strip().upper()
        self.chain_id       =       line[ 21  ].strip()
        self.res_number     = int(  line[22:26].strip())
        self.insert_code    =       line[ 26  ].strip()
        self.x_coordinate   = float(line[30:38].strip())
        self.y_coordinate   = float(line[38:46].strip())
        self.z_coordinate   = float(line[46:54].strip())
        self.occupancy      = float(line[54:60].strip())
        self.temp_factor    = float(line[60:66].strip())
        self.seg_id         =       line[72:76].strip()
        self.element        =       line[76:78].strip()
    def pdb_line(self):
        line = (
              "{0:<6.6}".format(                self.atom_type    )
            +   "{0:>5}".format(                self.atom_number  )
            + " "                                                  
            + "{0:>4.4}".format("{0:3}".format( self.atom_name  ) )
            + "{0:<1.1}".format(                self.alt_id       )
            + "{0:>3.3}".format(                self.res_name     )
            + " "                                                  
            + "{0:<1.1}".format(                self.chain_id     )
            +   "{0:>4}".format(                self.res_number   )
            + "{0:<1.1}".format(                self.insert_code  )
            + "   "                                                
            + "{0:>8.3f}".format(                self.x_coordinate )
            + "{0:>8.3f}".format(                self.y_coordinate )
            + "{0:>8.3f}".format(                self.z_coordinate )
            + "{0:>6.2f}".format(                self.occupancy    )
            + "{0:>6.2f}".format(                self.temp_factor  )
            + "      "                                             
            + "{0:<4.4}".format(                self.seg_id       )
            + "{0:>2.2}".format(                self.element      )
            )
        return line
    
    
    
    
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
    print("{0:<30.30}{1}".format("ATOM: "               , fields[0]))        # 0  ATOM
    print("{0:<30.30}{1}".format("Atom Number: "        , fields[1]))        # 1  Atom Serial Number
    print("{0:<30.30}{1}".format("Atom Name: "          , fields[2]))        # 2  Atom Name
    print("{0:<30.30}{1}".format("Alt Location: "       , fields[3]))        # 3  Alternate Location Indicator
    print("{0:<30.30}{1}".format("Residue Name: "       , fields[4]))        # 4  Residue Name
    print("{0:<30.30}{1}".format("Chain Id: "           , fields[5]))        # 5  Chain Identifier
    print("{0:<30.30}{1}".format("Res Number: "         , fields[6]))        # 6  Residue Sequence Number
    print("{0:<30.30}{1}".format("Insertion Code: "     , fields[7]))        # 7  Insertion Codes of Residues
    print("{0:<30.30}{1}".format("X Coordinate: "       , fields[8]))        # 8  X Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Y Coordinate: "       , fields[9]))        # 9  Y Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Z Coordinate: "       , fields[10]))       # 10 Z Orthogonal A Coordinate
    print("{0:<30.30}{1}".format("Occupancy: "          , fields[11]))       # 11 Occupancy
    print("{0:<30.30}{1}".format("Temperature Factor: " , fields[12]))       # 12 Temperature Factor
    print("{0:<30.30}{1}".format("Seg Id: "             , fields[13]))       # 13 Segment Identifier
    print("{0:<30.30}{1}".format("Element: "            , fields[14]))       # 14 Element Symbol

def pdb_atom_to_line(fields):
    # Check Types
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
              "{0:<6.6}".format(                self.atom_type    )
            +   "{0:>5}".format(                self.atom_number  )
            + " "                                                  
            + "{0:>4.4}".format("{0:3}".format( self.atom_name  ) )
            + "{0:<1.1}".format(                self.alt_id       )
            + "{0:>3.3}".format(                self.res_name     )
            + " "                                                  
            + "{0:<1.1}".format(                self.chain_id     )
            +   "{0:>4}".format(                self.res_number   )
            + "{0:<1.1}".format(                self.insert_code  )
            + "   "                                                
            + "{0:>8.3f}".format(                self.x_coordinate )
            + "{0:>8.3f}".format(                self.y_coordinate )
            + "{0:>8.3f}".format(                self.z_coordinate )
            + "{0:>6.2f}".format(                self.occupancy    )
            + "{0:>6.2f}".format(                self.temp_factor  )
            + "      "                                             
            + "{0:<4.4}".format(                self.seg_id       )
            + "{0:>2.2}".format(                self.element      )
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
