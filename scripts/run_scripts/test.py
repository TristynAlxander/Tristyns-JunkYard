# Python Imports
import sys
import os

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from dat_functions import DatFileDict
from seq_functions import AnalyzeSeq
from str_functions import StringPath



    
a = "asdfgrth etyjnrjh rytj retyj etyj rtyj rty jety jety j This article is protected by copyrigt. ags ertghwe thr t"

b = truncate_over(a)
print(b)


#my_str.find(sub[, start[, end]] )

"""
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.                # File Paths
    my_file_path    = os.path.abspath(sys.argv[1])                  #
    a = StrPath(my_file_path)
    print(a.file_to_str())
"""