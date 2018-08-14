### Imports ###

import sys
import os
import shutil

current_dir     = os.path.dirname(os.path.realpath(__file__))+"/"   # 
westpa_classes  = current_dir+"lib/classes/"                        # 
sys.path.insert(0, westpa_classes)                                  # 

import common




class BStates:
    
    START_STR   = common.strip_line_lead("        ","""
    ### START ###                                           #
                                                            #
    if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging 
        set -x                                              # Display Commands
        env | sort                                          # Display Environment Variables (sorts)
    fi                                                      #
                                                            #
    source $WEST_SIM_ROOT/env/env.sh                        # Load Environmental Variables.
                                                            #
    cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                            #
    ### /START ###                                          #
    """)
    
    LINK_STR   = common.strip_line_lead("        ","""
    ### Link Bstates
    mkdir -p $(dirname $WEST_ISTATE_DATA_REF)           # Make Directory (with parents, as needed) of Path
    ln -s $WEST_BSTATE_DATA_REF $WEST_ISTATE_DATA_REF   # Symlinking original(basis states) new(initial states)
    """)
    
    GEN_ISTATE_START   = common.strip_line_lead("        ",
        """
        #!/bin/bash
        
        ### START ###                                           #
                                                                #
        if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging 
            set -x                                              # Display Commands
            env | sort                                          # Display Environment Variables (sorts)
        fi                                                      #
                                                                #
        source $WEST_SIM_ROOT/env/env.sh                        # Load Environmental Variables.
                                                                #
        cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                                #
        ### /START ###                                          #
        """)
    GEN_ISTATE_SYMLINK = common.strip_line_lead("        ",
        """
        ### Link Bstates
        mkdir -p $(dirname $WEST_ISTATE_DATA_REF)           # Make Directory (with parents, as needed) of Path
        ln -s $WEST_BSTATE_DATA_REF $WEST_ISTATE_DATA_REF   # Symlinking original(basis states) new(initial states)
        """)
    
    
    
    
    def __init__(self, root=""):
        self.bstate_paths = []                                                      # Instantiate paths
        self.west_root    = root                                                    # Instantiate west_root
    
    def __bstates__(self):
        
        bstate_list = []
        
        all_lists = common.all_type(self.bstate_paths,list)
        all_str   = common.all_type(self.bstate_paths,str)
        
        if(all_str):
            bstate_list.append("0 1 initial")
        elif(all_lists):
            frac = 1.0/float(len(self.bstate_paths))
            i = 0
            for b_list in self.bstate_paths:
                bstate_list.append(str(1.0-frac)+" "+str(frac)+" "+str(i)+"_initial")
            # TODO Fix this
            print("bstate.txt probably isn't right.")
        else:
            print("Bad bstate paths.")
            print("Needs either list of all list or list of all strs")
        
        return bstate_list
    
    def __prep_files__(self):
        
        # Make init_states/
        init_dir = self.west_root+"/init_states"                                    # Directory Name
        if(not os.path.isdir(init_dir)):                                            # If No Directory
            os.makedirs(init_dir)                                                   # Make Directory
        
        # Make basis_states/
        bstates_dir = init_dir+"/basis_states"                                      # Directory Name
        if(not os.path.isdir(bstates_dir)):                                         # If No Directory
            os.makedirs(bstates_dir)                                                # Make Directory
        
        
        all_lists = common.all_type(self.bstate_paths,list)
        all_str   = common.all_type(self.bstate_paths,str)
        
        if(all_lists):
            i = 0
            for b_list in self.bstate_paths:
                # Make initial/
                istates_dir = bstates_dir+"/"+str(i)+"_initial"                     # Directory Name
                if(not os.path.isdir(istates_dir)):                                 # If No Directory
                    os.makedirs(istates_dir)                                        # Make Directory
                
                # Replace bstate Path Files                                         # Replace bstate Path Files
                for path in b_list:                                                 # 
                    
                    path_fix  = common.fix_file_path(path)                          # Fix File Path
                    path      = path_fix["path"]                                         # Get Path
                    file_name = path_fix["name"]                                         # Get Name
                    w_path    = istates_dir+"/"+file_name                           # Define westpa path
                    
                    if(os.path.isfile(w_path)):                                     # If file exist
                        os.remove(w_path)                                           # Remove it.
                    shutil.copyfile(path, w_path)                                       # Copy File
                
        elif(all_str):
            
            # Make initial/
            istates_dir = bstates_dir+"/initial"                                    # Directory Name
            if(not os.path.isdir(istates_dir)):                                     # If No Directory
                os.makedirs(istates_dir)                                            # Make Directory
            
            # Replace bstate Path Files                                             # Replace bstate Path Files
            for path in self.bstate_paths:                                          # 
                
                path_fix  = common.fix_file_path(path)                              # Fix File Path
                path      = path_fix["path"]                                             # Get Path
                file_name = path_fix["name"]                                             # Get Name
                w_path    = istates_dir+"/"+file_name                               # Define westpa path
                
                if(os.path.isfile(w_path)):                                         # If file exist
                    os.remove(w_path)                                               # Remove it.
                shutil.copyfile(path, w_path)                                           # Copy File
                
        else:
            print("Bad bstate paths.")
            print("Needs either list of all list or list of all strs")
        
    def make_bstates_scripts(self):                                                         # Make bstates File
        
        # File Prep                                                                 # File Prep
        BStates.__prep_files__(self)                                                # 
        
        # Make bstates_str                                                          ### Make bstates_str ###
        bstates     = BStates.__bstates__(self)                                     # Make bstates lines Statements
        bstates_str = ""                                                            # Start with Nothing
        for istate in bstates:                                                      # Add each line
            bstates_str = bstates_str + istate+"\n"                                 # 
        
        # Write bstates.txt                                                         ### Write bstates.txt ###
        w_bstates   = self.west_root+"/init_states/basis_states/bstates.txt"        # Define bstates.txt path
        bstates_txt = open(w_bstates,"w+")                                          # Open/Create
        bstates_txt.write(bstates_str)                                              # Write
        bstates_txt.close()                                                         # Close
        
        # Make gen_istate.sh
        gen_istate = BStates.START_STR + BStates.LINK_STR
        w_gen_istate   = self.west_root+"/init_states/gen_istate.sh"                # Define gen_istate.sh path
        bstates_txt = open(w_bstates,"w+")                                          # Open/Create
        bstates_txt.write(bstates_str)                                              # Write
        bstates_txt.close()                                                         # Close
        
        
        
