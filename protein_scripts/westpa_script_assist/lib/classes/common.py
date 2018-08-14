import sys
import os
import shutil

def safe_recursive_copy(old_path,new_path):
    
    old = fix_file_path(old_path)
    new = fix_file_path(new_path)
    
    if(os.path.isdir(old["path"])):
        os.makedirs(new["path"])
        paths = os.listdir(old["path"])
        for path in paths:
            print(old["path"]+"/"+path)
            safe_recursive_copy(old["path"]+"/"+path,new["path"]+"/"+path.split("/")[-1])
    elif(os.path.isfile(old["path"])):
        shutil.copyfile(old["path"], new["path"])
    # Else Nothing


def fix_file_path(file_path):
    file_path = file_path.replace("\\","/")                                             # Fix Slashes
    
    while("//" in file_path):
        file_path = file_path.replace("//","/")                                         # Fix Slashes
    
    if(":" in file_path[:2]):                                                           # If Bad Drive        E.g:  D:/
        new_drive = "/mnt/"+file_path[:2].replace(":","").lower()                       #   Fix Drive Prefix  E.g:  /mnt/d
        file_path = new_drive+file_path[2:]                                             #   Fix Path
    
    file_name   = file_path.split("/")[-1]                                              # Isolate File Name
    if("." in file_name):
        dot_index   = file_name.find(".")                                               # Find start of suffix 
        file_suffix = file_name[dot_index:]                                             # Isolate suffix
    else:
        file_suffix = ""
    
    if(os.path.isdir(file_path)):
        if(file_path[-1]!="/"):
            file_path=file_path+"/"
    
    file_dir = ""
    if(os.path.isdir(file_path)):
        file_dir = file_path
    elif(os.path.isfile(file_path)):
        a = (len(file_path)-len(file_name))
        file_dir = file_path[:a]
    
    return {"path":file_path,"name":file_name,"suffix":file_suffix,"dir":file_dir,"directory":file_dir}

def get_var_name(var_name,var_name_list,constant=False):
    
    # Convert to Variable Format                            ### Convert to Variable Format ###
    var_name   = var_name.split("/")[-1].replace(".","_")   # After Slashes, Replace Periods with Underscores
    if(constant):                                           # Constants are Uppercase
        var_name = var_name.upper()                         #
    else:                                                   # Non-Constants are lowercase
        var_name = var_name.lower()                         # 
    # Make Unique Suffix                                    ### Make Unique Suffix ###
    if(var_name in var_name_list):                          # If Variable Name already exist
        i=1                                                 # Start Suffix Count
        while(var_name+str(i) in var_name_list):            # while the name is still taken
            i=i+1                                           # Increment Count 
        var_name = var_name+str(i)                          # Accept Untaken Name
    
    return var_name

def strip_line_lead(lead,string):
    i = len(lead)
    string_array = string.split("\n")
    string = ""
    for line in string_array:
        line   = line[i:].rstrip()+"\n"
        string = string + line
    return string

def all_type(my_list,my_type):
    all_lists = True                                                  # Check is Every Element in List is a list
    for i in my_list:                                                 #  
        all_lists = all_lists and (type(i) is my_type)                # 
    return all_lists

if (__name__ == "__main__"):
    string_list = ["a","b","c"]
    list_list = [["a"],["a","b","c"],["a","c"],"f"]
    #print(all_type(list_list,list))
    nf = "new_file"
    if(os.path.exists(nf)):
        if(os.path.isfile(nf)):
            os.remove(nf)
        if(os.path.isdir(nf)):
            os.rmdir(nf)
    safe_recursive_copy("./","../new_file")
    
