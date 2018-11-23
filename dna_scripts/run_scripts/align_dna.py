# Python Imports
import sys
import os
# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from dna_functions import PrettyDNA
from dna_functions import AnalyzeDNA

# Functions
# No File-Specific Functions

# Import and Main Scripts
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    master_seq_file = os.path.abspath(sys.argv[1])
    align__seq_file = os.path.abspath(sys.argv[2])
    
    master_seq = PrettyDNA.simplify_seq(open(master_seq_file, 'r').read())
    align__seq = PrettyDNA.simplify_seq(open(align__seq_file, 'r').read())
    
else:
    master_seq = ""
    align__seq = ""

AnalyzeDNA.print_align(master_seq,align__seq)
