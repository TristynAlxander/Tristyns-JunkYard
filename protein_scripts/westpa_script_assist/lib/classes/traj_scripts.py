### Imports ###

import sys
import os
import shutil

current_dir     = os.path.dirname(os.path.realpath(__file__))+"/"   # 
westpa_classes  = current_dir+"lib/classes/"                        # 
sys.path.insert(0, westpa_classes)                                  # 

import common


class TrajScripts:
    
    
    START  = common.strip_line_lead("        ",
        """
        #!/bin/bash
        ### START ###                                           #
                                                                #
        if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging 
            set -x                                              # Display Commands
            env | sort                                          # Display Environment Variables (sorted)
        fi                                                      #
                                                                #
        source $WEST_SIM_ROOT/env/env.sh                        # Load Environmental Variables.
                                                                #
        cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                                #
        ### /START ###                                          #
        """)
    END    = common.strip_line_lead("        ",
        """
        ### END ###                                             #
                                                                #
        cd $WEST_SIM_ROOT                                       # Go to Simulation Root
                                                                #
        if [ -n "$SEG_DEBUG" ] ; then                           # If we're Debugging
          head -v $WEST_PCOORD_RETURN                           #
        fi                                                      #
                                                                #
        ### /END ###                                            #
        """)
    
    
    def __init__(self, root=""):
        self.west_root   = root                                                     # Instantiate west_root
        self.pcoord_dirs = []                                                       # Instantiate Dir List
        self.aux_dirs    = [] 
        self.env         = None
        
    
    def __prep_pcoord_files__(self):
        
        # Make init_states/
        init_dir = self.west_root+"/init_states"                                    # Directory Name
        if(not os.path.isdir(init_dir)):                                            # If No Directory
            os.makedirs(init_dir)                                                   # Make Directory
        
        # Make init_states/init_pcoord/
        init_pcoord_dir = init_dir+"/init_pcoord"                                   # Directory Name
        if(not os.path.isdir(init_pcoord_dir)):                                     # If No Directory
            os.makedirs(init_pcoord_dir)                                            # Make Directory
        
        # Make pcoord/
        pcoord_dir = self.west_root+"/pcoord"                                       # Directory Name
        if(not os.path.isdir(pcoord_dir)):                                          # If No Directory
            os.makedirs(pcoord_dir)                                                 # Make Directory
        
        i=0
        for pcoord in self.pcoord_dirs:
            # Make pcoord/x_pcoord/
            i_pcoord_dir = pcoord_dir+"/"+str(i)+"_pcoord"                          # Directory Name
            if(os.path.isdir(i_pcoord_dir)):                                        # If No Directory
                os.remove(i_pcoord_dir)                                             # Remove Directory
            shutil.copytree(pcoord,i_pcoord_dir)                                    # Copy Recursively
            
            # Make init_pcoord/x_ipcoord/
            ii_pcoord_dir = init_pcoord_dir+"/"+str(i)+"_ipcoord"                   # Directory Name
            if(os.path.isdir(ii_pcoord_dir)):                                       # If No Directory
                os.remove(ii_pcoord_dir)                                            # Remove Directory
            shutil.copytree(pcoord,ii_pcoord_dir)                                   # Copy Recursively
        
        
        # Segment Directory                                                             # Segment Directory 
        seg_scripts_dir = self.west_root+"/seg_scripts"                                 # Directory Name
        if(not os.path.isdir(seg_scripts_dir)):                                         #
            os.makedirs(seg_scripts_dir)                                                # Make Directory
    
    def __prep_aux_files__(self):
        
        # Make init_states/
        init_dir = self.west_root+"/init_states"                            # Directory Name
        if(not os.path.isdir(init_dir)):                                    # If No Directory
            os.makedirs(init_dir)                                           # Make Directory
        
        # Make init_states/init_aux_coord/
        init_aux_dir = init_dir+"/init_aux_coord"                           # Directory Name
        if(not os.path.isdir(init_aux_dir)):                                # If No Directory
            os.makedirs(init_aux_dir)                                       # Make Directory
        
        
        # Make aux_coord/
        aux_dir = self.west_root+"/aux_coord"                               # Directory Name
        if(not os.path.isdir(aux_dir)):                                     # If No Directory
            os.makedirs(aux_dir)                                            # Make Directory
        
        i=0
        for aux in self.aux_dirs:
            # Make aux_coord/x__aux_coord/
            i_aux_dir = aux_dir+"/"+str(i)+"_aux_coord"                     # Directory Name
            if(os.path.isdir(i_aux_dir)):                                   # If No Directory
                os.remove(i_aux_dir)                                        # Remove Directory
            shutil.copytree(aux,i_aux_dir)                                  # Copy Recursively
            
            # Make init_aux_coord/x_iaux_coord/
            ii_aux_dir = init_aux_dir+"/"+str(i)+"_iaux_coord"              # Directory Name
            if(os.path.isdir(ii_aux_dir)):                                  # If No Directory
                os.remove(ii_aux_dir)                                       # Remove Directory
            shutil.copytree(aux,ii_aux_dir)                                 # Copy Recursively
            
    def __env_ln__(self,current_dir):
        env_ln = []
        if(self.env.env_vars == [] or self.env.env_vars == None):
            print("Need Environment Variables.")
        else:
            for env_var in self.env.env_vars:
                ln = "ln -sf {0:<50} {1:<} || exit 1\n".format("$"+env_var,current_dir)
                env_ln.append(ln)
        return env_ln
    
    def __env_rm__(self,current_dir):
        env_rm = []
        if(self.env.env_vars == [] or self.env.env_vars == None):
            print("Need Environment Variables.")
        else: 
            for env_var in self.env.env_vars:
                rm = "rm -r {0:<50} || exit 1\n".format(current_dir+"$"+env_var)
                env_rm.append(rm)
    
    def make_traj_scripts(self):                                                             # Make Environment File
        
        ### Initial Progress Coordinate ###                                                 ### Initial Progress Coordinate ###
        
        init_pcoord_str = TrajScripts.START                                                 # Start String
        
        # Add Environment Vars to each Progress Coordinate                                  ### Add Environment Vars to each Progress Coordinate ###
        i=0                                                                                 # Initialize Directory Counter
        for pcoord_dir in self.pcoord_dirs:                                                 # Add Environment Vars to each Progress Coordinate 
            ith_pcoord_dir = "$WEST_SIM_ROOT/init_states/init_pcoord/"+str(i)+"_ipcoord"    # Get Directory
            env_ln = TrajScripts.__env_ln__(self,ith_pcoord_dir)                            # Get Link Strings
            for ln in env_ln:                                                               # Add each 
                init_pcoord_str = init_pcoord_str + ln                                      # 
            i=i+1                                                                           # Increment Directory Counter
        
        # Add Environment Vars to Auxiliary Coordinates                                     ### Add Environment Vars to Auxiliary Coordinates ###
        i=0                                                                                 # Initialize Directory Counter
        for aux_dir in self.aux_dirs:                                                       # 
            ith_aux_dir = "$WEST_SIM_ROOT/init_states/init_aux_coord/"+str(i)+"_iaux_coord" # Get Directory
            env_ln = TrajScripts.__env_ln__(self,ith_aux_dir)                               # Get Link Strings
            for ln in env_ln:                                                               # Add each
                init_pcoord_str = init_pcoord_str + ln                                      # 
            i=i+1                                                                           # Increment Directory Counter
        
        # TODO: Add pcoords and aux_data appropriately
        
        init_pcoord_str = init_pcoord_str+ TrajScripts.END                                  # End String
        
        # Write init_pcoord.sh                                                              ### Write init_pcoord.sh ###
        init_pcoord     = self.west_root+"/init_states/init_pcoord.sh"                      # Define init_pcoord.sh path
        init_pcoord_txt = open(init_pcoord,"w+")                                            # Open/Create
        init_pcoord_txt.write(init_pcoord_str)                                              # Write
        init_pcoord_txt.close()                                                             # Close
        
        
        
        
        
        ### Pre Segment Iteration Script ###                                            ### Pre Segment Iteration Script ###
        
        pre_iter_str = TrajScripts.START
        
        # Add Environment Vars to each Progress Coordinate                              ### Add Environment Vars to each Progress Coordinate ###
        i=0                                                                             # Initialize Directory Counter
        for pcoord_dir in self.pcoord_dirs:                                             # Add Environment Vars to each Progress Coordinate 
            ith_pcoord_dir = "$WEST_SIM_ROOT/pcoord/"+str(i)+"_pcoord/"                 # Get Directory
            env_ln = TrajScripts.__env_ln__(self,ith_pcoord_dir)                        # Get Link Strings
            for ln in env_ln:                                                           # Add each 
                pre_iter_str = pre_iter_str + ln                                        # 
            i=i+1                                                                       # Increment Directory Counter
        
        # Add Environment Vars to Auxiliary Coordinates                                 ### Add Environment Vars to Auxiliary Coordinates ###
        i=0                                                                             # Initialize Directory Counter
        for aux_dir in self.aux_dirs:                                                   # 
            ith_aux_dir = "$WEST_SIM_ROOT/aux_coord/"+str(i)+"_aux_coord/"              # Get Directory
            env_ln = TrajScripts.__env_ln__(self,ith_aux_dir)                           # Get Link Strings
            for ln in env_ln:                                                           # Add each
                pre_iter_str = pre_iter_str + ln                                        # 
            i=i+1                                                                       # Increment Directory Counter
        
        # TODO: Add pcoords and aux_data appropriately
        
        pre_iter_str = pre_iter_str + TrajScripts.END
        
        # Write pre_iter.sh                                                             ### Write pre_iter.sh ###
        pre_iter     = self.west_root+"/seg_scripts/pre_iter.sh"                        # Define pre_iter.sh path
        pre_iter_txt = open(pre_iter,"w+")                                              # Open/Create
        pre_iter_txt.write(pre_iter_str)                                                # Write
        pre_iter_txt.close()                                                            # Close
        
        
        
        #
        # pre_iter.sh
            # Link All the files appropriately
            # Link All Environment Variables
            # If
        # runseg.sh
            # Run Progress coordinates
            # Run Auxillary 
        # post_iter.sh
            # Remove all the links
        # init_pcoord.sh
        #