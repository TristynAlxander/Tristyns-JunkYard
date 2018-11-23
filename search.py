import os
import sys

SEARCH_EXTENSIONS = (
    ".txt",
    ".md",
    ".xml",
    ".svg",
    ".py",
    ".bat"
    )

    
def tattle(path,my_str):
    if(my_str.find("\t")!=-1):
        print("There's a tab in:"+path)
    
def search(search_term, directory,supress=True,case_sensitive=False):   # 
    result_list = []                                                    # 
    for (dirpath, dirnames, file_names) in os.walk(directory):          # Walk Directories 
        for file_name in file_names:                                    # Walk Files       
            # Set Variables                                             # Set Variables 
            file_path  = (dirpath+"/"+file_name)                        #
            searchable = file_path.lower().endswith(SEARCH_EXTENSIONS)  #
            result = False                                              #
            # Search                                                                            # Search
            if(searchable):                                                                     #
                try:                                                                            #
                    file = open(file_path,"r")                                                  #
                    for line in file:                                                           #
                        if(not supress):                                                        #
                            tattle(file_path,line)                                              #
                        if(not case_sensitive):                                                 # Adjust Line
                            line        = line.lower()                                          #
                            search_term = search_term.lower()                                   #
                        normal_line   = line.strip()                                            # 
                        under_line    = line.strip().replace(" ","_").replace("\t","__")        #
                        normal_search = normal_line.find(search_term)                           # Search 
                        under_serach  =  under_line.find(search_term)                           #
                        if(normal_search != -1 or under_serach != -1):                          # Set Result (Indirectly)
                            result = True                                                       #   Var for file, not lines
                    file.close()                                                                #
                except ValueError:                              
                    if(not supress):
                        print("this file broke the search: "+file_path)
            # Report Results
            if(result):
                result_list.append(file_path)
    return result_list
            
            
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    search_term = sys.argv[1]
    directory = os.getcwd()
    for x in search(search_term,directory,supress=True,case_sensitive=False):
        print(x)
else: 
    search_term = "k_B"
    directory = os.getcwd()
    for x in search(search_term,directory,supress=True,case_sensitive=False):
        print(x)