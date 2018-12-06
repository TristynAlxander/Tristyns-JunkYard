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
    # sys.argv[0] is this script, so don't count it.                # File Paths
    seq_file        = os.path.abspath(sys.argv[1])                  #
    seq_file_f      = os.path.abspath(sys.argv[2])                  #
    seq_file_r      = os.path.abspath(sys.argv[3])                  #
    if(len(sys.argv)>5):                                            # Save Files
        save_f   = sys.argv[4]                                      #   Given Forward
        save_r   = sys.argv[5]                                      #   Given Reverse
    else:                                                           #
        pars_file = StringPath(seq_file)                            #
        save_f = pars_file.file_root+"_align_f"+pars_file.suffix    #   Derive Forward
        save_r = pars_file.file_root+"_align_r"+pars_file.suffix    #   Derive Reverse
        
    seq   = PrettySeq.simplify_seq(open(seq_file  , 'r').read())    # Main    Sequence
    seq_f = PrettySeq.simplify_seq(open(seq_file_f, 'r').read())    # Forward Sequence
    seq_r = PrettySeq.simplify_seq(open(seq_file_r, 'r').read())    # Reverse Sequence
    
else:                                                               # Custom Inputs 
    seq       = ""
    seq_f     = ""
    seq_r     = ""
    save_f    = ""
    save_r    = ""


seq_rc = AnalyzeSeq.dna_reverse_complement(seq_r)                   # Get Reverse Complement1

open(save_f, 'w+').write(AnalyzeSeq.align_str(seq,seq_f)[0])        # Write Forward Alignment 
open(save_r, 'w+').write(AnalyzeSeq.align_str(seq,seq_rc)[0])       # Write Reverse Alignment



