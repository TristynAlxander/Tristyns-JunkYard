# Imports
import os
import sys
from html.parser import HTMLParser

class StringFunctions:
    
    def __strip_lead_by_int__(string,lead_int,ws_strip=True):
        if(ws_strip):
            string = string.strip()
        string = string[lead_int:]
        if(ws_strip):
            string = string.strip()
        return string
    def __strip_lead_by_str__(string,lead_str,ws_strip=True):
        if(ws_strip):
            string   = string.strip()
            lead_str = lead_str.strip()
        i = string.find(lead_str)
        if(i == 0):
            string = string[len(lead_str):]
        if(ws_strip):
            string   = string.strip()
        return string
    def strip_lead(string,lead,ws_strip=True):
        if(type(lead) == int):
            return StringFunctions.__strip_lead_by_int__(string,lead,ws_strip=ws_strip)
        elif(type(lead) == str):
            return StringFunctions.__strip_lead_by_str__(string,lead,ws_strip=ws_strip)
    
    #Common Split One Liners
    #string_list = my_function(x) for x in my_string.split(delimiter)                                               # Run Function on split parts
    #my_string   = my_string.split(cut_str)[1] if len(my_string.split(cut_str))>1 else my_string.split(cut_str)[0]  # If Cut, take suffix
    
    def is_float(my_str):
        try:
            float(my_str)
            return True
        except ValueError:
            return False
        
    
    def safe_name(my_name,conflict_list=[],constant=False):    
        # Safe Characters                                       # Safe Characters
        my_name   = my_name.replace(".","_")                    #   Replace Periods with Underscores
        my_name   = my_name.replace("/","_")                    #   Replace Slashes with Underscores
        # Capitalization Conventions                            # Capitalization Conventions
        if(constant):                                           #   Constants are Uppercase
            my_name = my_name.upper()                           #
        else:                                                   #   Non-Constants are lowercase
            my_name = my_name.lower()                           # 
        # Make Unique Suffix                                    # Make Unique Suffix
        if(my_name in conflict_list):                           #   Check Other Names
            i=0                                                 #   Start Suffix Count
            while(my_name+str(i) in conflict_list):             #   Increment Count Until Unique
                i=i+1                                           # 
            my_name = my_name+str(i)                            # 
        return my_name
    
    def write_str_list(my_list,prefix_str="",suffix_str=""):            # Coverts lists of strings to files
        for i,item in enumerate(my_list):                               # For each String
            my_file = open(prefix_str+str(i)+suffix_str+".txt", 'w+')   # Make file
            my_file.write(item)                                         # write string
            my_file.close()                                             # Close file
    
    def less_whitespace(my_str):
        my_str = my_str.replace("\n", " ")
        my_str = my_str.replace("\t", " ")
        while("  " in my_str):
            my_str = my_str.replace("  ", " ")
        return my_str
    def remove_whitespace(my_str):
        my_str = my_str.replace(" ","")
        my_str = my_str.replace("\r","")
        my_str = my_str.replace("\n","")
        my_str = my_str.replace("\t","")
        return my_str
    
    def simplify_str(my_str):
        my_str = my_str.lower()
        my_str = StringFunctions.remove_whitespace(my_str)
        return my_str
    
    def remove_brackets(my_str,left="[",right="]"):
        my_bracket_list = []
        my_str_list = []
        
        while(left in my_str and right in my_str):
            l = my_str.find(left)
            r = my_str.find(right,l)
            my_bracket_list.append(my_str[l+1:r])
            my_str_list.append(my_str[:l])
            my_str = my_str[r+1:]
        my_str_list.append(my_str)
        
        return my_str_list, my_bracket_list
    
    def truncate(my_str,i=75):
        if(len(my_str) > i):
            my_str = my_str[:i] + '...'
        return my_str
    def truncate_over(main_str,over_str="copyright",e=30):
        i = main_str.find(over_str)-30 if main_str.find(over_str)!=-1 else -1
        if(len(main_str) > i and i !=-1):
            main_str = main_str[:i] + '...'
        return main_str
        
        
        
    
class StringPath:
    def __init__(self, file_path):
        # Variable List
        #   is_dir
        #   file_path
        #   drive
        #   file_name
        #   file_dir
        #   file_root
        #   suffix
        
        self.file_path = file_path.replace("\\","/")                                        # Fix Slash Direction
        while("//" in file_path):                                                           # Fix Slash Doubling
            self.file_path = self.file_path.replace("//","/")                               #
        
        self.drive = ""
        if(":" in self.file_path[:2]):                                                      # Check Drive Name
            self.drive = self.file_path[:2].replace(":","").lower()                         #   Get Drive Letter
            self.file_path = "/mnt/"+self.drive+self.file_path[2:]                          #   Fix Drive Name
        elif("/mnt/" in self.file_path[:5]):                                                #
            self.drive = self.file_path[:2].replace("/mnt/","").lower()                     #   Get Drive Letter
        
        self.is_dir = False
        if(os.path.isdir(file_path) and (file_path[-1]!="/")):                              # Fix Dir  Name
            file_path   = file_path+"/"                                                     # 
            self.is_dir = True                                                              #
        
        self.file_name = file_path.split("/")[-1]                                           # Get File Name
        if(self.file_name == ""):                                                           # Get Dir  Name
            self.file_name = file_path.split("/")[-2]                                       # 
            self.is_dir = True                                                              # 
        
        if(self.is_dir):
            self.file_dir  = self.file_path                                                 # Dir as Path  
            self.file_root = self.file_name                                                 # Root as Name
            self.suffix    = ""                                                             # Empty Suffix
        else:
            self.file_dir = self.file_path[:(len(self.file_path)-len(self.file_name))]
            if("." in self.file_name):                                                      # Get Suffix & Root
                dot_index      = self.file_name.find(".")                                   #   Suffix Start
                self.file_root = self.file_name[:dot_index]                                 #   Isolate Root
                self.suffix    = self.file_name[dot_index:]                                 #   Isolate Suffix
            else:                                                                           #
                self.file_root = self.file_name                                             #   Root as Name
                self.suffix    = ""                                                         #   Empty Suffix

    def file_to_str(self):
        my_str = ""
        for line in open(self.file_path,"r"):
            my_str = my_str+line
        return my_str

class HTMLStrParser(HTMLParser):
    def __init__(self,html_str):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.data = []
        self.md_data = []
        self.feed(html_str)
    def handle_starttag(self, tag, attrs):
        if(  tag == "p"):
            self.md_data.append("\n\n")
        elif(tag == "b"):
            self.md_data.append("**")
        elif(tag == "sub"):
            self.md_data.append("\_")
        elif(tag == "sup"):
            self.md_data.append("^^")
        elif(tag == "em"):
            self.md_data.append("_")
        elif(tag == "h1"):
            self.md_data.append("#")
        elif(tag == "h2"):
            self.md_data.append("##")
        elif(tag == "h3"):
            self.md_data.append("###")
        elif(tag == "h4"):
            self.md_data.append("####")
        elif(tag == "h5"):
            self.md_data.append("#####")
        elif(tag == "h6"):
            self.md_data.append("######")
        
    def handle_endtag(self, tag):
        if(  tag == "p"):
            self.md_data.append("\n\n")
        elif(tag == "b"):
            self.md_data.append("**")
        elif(tag == "sub"):
            self.md_data.append(" ")
        elif(tag == "sup"):
            self.md_data.append(" ")
        elif(tag == "em"):
            self.md_data.append("_")
        elif(tag == "h1"):
            self.md_data.append("\n\n")
        elif(tag == "h2"):
            self.md_data.append("\n\n")
        elif(tag == "h3"):
            self.md_data.append("\n\n")
        elif(tag == "h4"):
            self.md_data.append("\n\n")
        elif(tag == "h5"):
            self.md_data.append("\n\n")
        elif(tag == "h6"):
            self.md_data.append("\n\n")
            
    def handle_data(self, data):
        self.data.append(data)
        self.md_data.append(data)
        
