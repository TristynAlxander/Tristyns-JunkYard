### Imports ###

import sys
import os
import shutil

current_dir     = os.path.dirname(os.path.realpath(__file__))+"/"   # 
westpa_classes  = current_dir+"lib/classes/"                        # 
sys.path.insert(0, westpa_classes)                                  # 

import common




class Env:
    
    ENV_STR   = common.strip_line_lead("        ",
        """
        #!/bin/sh
        ################################## WESTPA #######################################
        # Is WEST_ROOT set?                                                             #
        if [ -z "$WEST_ROOT" ]; then                                                    #
          echo "The environment variable WEST_ROOT is not set."                         #
          echo "Try running 'source westpa.sh' from the WESTPA installation directory"  #
          exit 1                                                                        #
        fi                                                                              #
                                                                                        #
        # If no Simulation Root Directory, make it current Directory                    #
        if [ -z "$WEST_SIM_ROOT" ]; then                                                #
          export WEST_SIM_ROOT="$PWD"                                                   #
        fi                                                                              #
                                                                                        #
        export SIM_NAME=$(basename $WEST_SIM_ROOT)                                      #
                                                                                        #
        #################################################################################
        """)
    EXPORTS_COMMENT = "################################## EXPORTS ######################################\n"
    
    def __init__(self, root=""):
        self.env_paths       = []                                                   # Instantiate paths
        self.west_root       = root                                                 # Instantiate west_root
        self.env_vars        = []
        self.__env_exports__ = []
    
    def __env_export__(self):                                                       # Load Export Statements
        
        # Lists                                                                     # Lists
        env_exports   = []                                                          #   Export Statements
        var_name_list = []                                                          #   Variable Names
        
        for path in self.env_paths:                                                 # For Path Make Export Statement
            
            path_fix  = common.fix_file_path(path)                                  # Fix File Path
            path      = path_fix["path"]                                            # Get Path
            file_name = path_fix["name"]                                            # Get Name
            
            var_name = common.get_var_name(file_name,var_name_list,constant=True)   # Get Unique Variable Name
            var_name_list.append(var_name)                                          # Append to Name List
            
            export_path      = "\"$WEST_SIM_ROOT/env/files/"+file_name+"\""         # Get    Export Path
            export_statement = "export "+var_name+"="+export_path+"\n"              # Get    Export Statement
            env_exports.append(export_statement)                                    # Append Export Statement
        
        self.__env_exports__ = env_exports
        self.env_vars        = var_name_list
        return env_exports
    
    def __prep_files__(self):
        
        # Make env/
        env_dir = self.west_root+"/env"                                             # Directory Name
        if(not os.path.isdir(env_dir)):                                             # If No Directory
            os.makedirs(env_dir)                                                    # Make Directory
        
        # Make env/files/
        env_files_dir = env_dir+"/files"                                            # Directory Name
        if(not os.path.isdir(env_files_dir)):                                       # If No Directory
            os.makedirs(env_files_dir)                                              # Make Directory
        
        # Remove env.sh
        w_env  = env_dir+"/env.sh"                                                  # Define env path
        if(os.path.isfile(w_env)):                                                  # If file exist
            os.remove(w_env)                                                        # Replace it.
        
        # Replace Env Path Files                                                    # Replace Env Path Files
        for path in self.env_paths:                                                 # 
            
            path_fix  = common.fix_file_path(path)                                  # Fix File Path
            path      = path_fix["path"]                                                 # Get Path
            file_name = path_fix["name"]                                                 # Get Name
            w_path = env_files_dir+"/"+file_name                                    # Define westpa path
            
            if(os.path.isfile(w_path)):                                             # If file exist
                os.remove(w_path)                                                   # Remove it.
            shutil.copyfile(path, w_path)                                               # Copy File
    
    def make_env_scripts(self):                                                             # Make Environment File
        
        # File Prep                                                                 # File Prep
        Env.__prep_files__(self)                                                    # 
        
        # Make Export Section                                                       ### Make Export Section ###
        env_exports = Env.__env_export__(self)                                      # Make Export Statements
        env_str     = Env.ENV_STR+Env.EXPORTS_COMMENT                               # Start with Initial plus Export Comment 
        for export in env_exports:                                                  # Add each export statement
            env_str = env_str + export                                              # 
        
        # Write env.sh                                                              ### Write env.sh ###
        w_env  = self.west_root+"/env/env.sh"                                       # Define env path
        env_sh = open(w_env,"w+")                                                   # Open/Create
        env_sh.write(env_str)                                                       # Write
        env_sh.close()                                                              # Close
        
