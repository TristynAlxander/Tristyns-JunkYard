import os
import sys
import math

def time_converter(path,factor):
    time_file = open(path)
    time_file_new = open(path+".new","w+")
    
    for line in time_file:
        fields = line.strip().split(":")                                   # Splits Columns
        min = float(fields[0]) + float(fields[1])/60.0
        new_min_frac = min*factor
        new_min = math.floor(new_min_frac)
        new_sec_frac = (new_min_frac-new_min)*60.0
        new_sec = math.floor(new_sec_frac)
        time_file_new.write("{0}:{1}\n".format(new_min,new_sec))
        
path    = os.path.abspath(sys.argv[1])          # Get File
i       = float(sys.argv[2])                    # Get In Number
time_converter(path,i)