# Python Imports
import sys
import os

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from conversion_functions import Concentrations

# Import and Main Scripts
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    sub_or_molar_mass   = sys.argv[1]
    molarity            = sys.argv[2]
else:
    sub_or_molar_mass   = ""
    molarity            = 0
    
g_per_L = Concentrations.mol_per_L_to_g_per_L(sub_or_molar_mass,molarity)
print(str(g_per_L)+" mg/mL")