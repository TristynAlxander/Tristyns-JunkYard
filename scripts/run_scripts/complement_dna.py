# Python Imports
import sys
import os

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from seq_functions import PrettySeq
from seq_functions import AnalyzeSeq
from str_functions import StringPath

# Import and Main Scripts
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    if(len(sys.argv) == 2):
        seq_file  = os.path.abspath(sys.argv[1])
        pars_file = StringPath(seq_file)
        save_file = pars_file.file_root+"_c"+pars_file.suffix
    elif(len(sys.argv) == 3):
        seq_file  = os.path.abspath(sys.argv[1])
        save_file = sys.argv[2]
    seq = PrettySeq.simplify_seq(open(seq_file, 'r').read())
    
else:
    seq         = ""
    save_file   = ""

open(save_file, 'w+').write(AnalyzeSeq.dna_reverse_complement(seq))
