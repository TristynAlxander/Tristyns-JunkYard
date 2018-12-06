# Python Imports
import sys
import os

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from str_functions import StringFunctions as str_f

class Concentrations:
    MOLAR_MASSES = {
        "Urea".lower():60.06,
        "EDTA".lower():292.24,
        "Tris".lower():121.14,
        "NaCl".lower():58.44
        }
    
    def __molar_to_g_per_L_num__(molar_mass,molarity):
        g_per_mol = float(molar_mass)                   # Convert to Floats
        mol_per_L = float(molarity)                     #
        g_per_L = g_per_mol*mol_per_L                   # Calculate
        return g_per_L
    def __molar_to_g_per_L_str__(substance,molarity):
        molar_mass = Concentrations.MOLAR_MASSES[substance.lower()]
        return Concentrations.__molar_to_g_per_L_num__(molar_mass,molarity)
        
    def mol_per_L_to_g_per_L(sub_or_molar_mass,molarity):
        sub_or_molar_mass = float(sub_or_molar_mass) if str_f.is_float(sub_or_molar_mass) else sub_or_molar_mass
        
        
        if(type(sub_or_molar_mass) == int):
            return Concentrations.__molar_to_g_per_L_num__(sub_or_molar_mass,molarity)
        elif(type(sub_or_molar_mass) == float):
            return Concentrations.__molar_to_g_per_L_num__(sub_or_molar_mass,molarity)
        elif(type(sub_or_molar_mass) == str):
            return Concentrations.__molar_to_g_per_L_str__(sub_or_molar_mass,molarity)
    