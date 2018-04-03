# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys



def average(*paths):
    # Initialize Files
    
    file_list = []
    for path in paths:
        pdb_old = open(path)                                        # Get  old PDB File
        fdata = [float(line.strip()) for line in pdb_old]
        file_list.append(fdata)
    
    average_list = []
    
    file_num = len(file_list)
    file_length = len(file_list[0])
    
    
    for i in range(0,file_length):
        sum = 0
        for file in file_list:
            sum=sum+float(file[i])
        avg = float(sum) / float(file_num)
        average_list.append(str(avg))
    return average_list
def list_to_dat(list,path):                     # 
    file = open(path,"w+")                      # 
    for item in list:                           # 
        file.write(str(item)+"\n")                        # 
    file.close()                                # 
 
if (__name__ == "__main__"):
    # sys.argv[0] is this script, so don't count it.
    
    
    
    average_list = average(
        os.path.abspath(sys.argv[1]),
        os.path.abspath(sys.argv[2]),
        os.path.abspath(sys.argv[3])
        )
    
    list_to_dat(average_list,"average_phi.dat")
    