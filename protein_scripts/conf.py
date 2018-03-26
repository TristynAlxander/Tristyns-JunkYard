if (__name__ == "__main__"):
    import os
    import sys

class NamdConf:
    
    SIM_NAME_STR_ARRAY = [
        "min_1",    # 0
        "min_2",    # 1
        "min_3",    # 2
        "min_4",    # 3
        "eq_1",     # 4
        "eq_2",     # 5
        "eq_3",     # 6
        "eq_4",     # 7
        "eq_5",     # 8
        "prod"      # 9
        ]
    TOPPAR_ARRAY = [
            "toppar/par_all36m_prot.prm",
            "toppar/par_all36_na.prm",
            "toppar/par_all36_carb.prm",
            "toppar/par_all36_lipid.prm",
            "toppar/par_all36_cgenff.prm",
            "toppar/toppar_all36_prot_retinol.str",
            "toppar/toppar_all36_na_rna_modified.str",
            "toppar/toppar_all36_carb_glycopeptide.str",
            "toppar/toppar_all36_prot_fluoro_alkanes.str",
            "toppar/toppar_all36_prot_na_combined.str",
            "toppar/toppar_all36_prot_heme.str",
            "toppar/toppar_all36_lipid_bacterial.str",
            "toppar/toppar_all36_lipid_miscellaneous.str",
            "toppar/toppar_all36_lipid_cholesterol.str",
            "toppar/toppar_all36_lipid_yeast.str",
            "toppar/toppar_all36_lipid_sphingo.str",
            "toppar/toppar_all36_lipid_inositol.str",
            "toppar/toppar_all36_lipid_cardiolipin.str",
            "toppar/toppar_all36_lipid_detergent.str",
            "toppar/toppar_all36_lipid_lps.str",
            "toppar/toppar_water_ions.str",
            "toppar/toppar_dum_noble_gases.str",
            "toppar/toppar_all36_na_nad_ppi.str",
            "toppar/toppar_all36_carb_glycolipid.str",
            "toppar/toppar_all36_carb_imlab.str"
            ]
    
    
    # Molecular Dynamics Engines
    CHARMM = 0
    AMBER  = 1
    
    def __init__(self, i, *args):
        self.stage           = i                                                        # Simulation Stage
        
        self.is_restart      = False
        self.first_time_step = 0
        self.init_sim        = (
            not self.is_restart and
            self.stage == 0
            )
        
        self.dis_temp        = (                                                        # Discontinuous Temperature
            (
            self.stage == 4 or                                                          # First Equilibration Step: Heating
            self.stage == 9                                                             # Production Run
            )
            and not self.is_restart
            )                                                                           # 
        self.heating         = (self.stage == 4)
        self.temperature     = 300
        
        
        self.md     = NamdConf.CHARMM                                                   # Molecular Dynamics Engine
        self.coords = "prep.pdb"
        self.parm   = "prep.psf"
        
        
        self.is_min = (
            self.stage == 0 or
            self.stage == 1 or
            self.stage == 2 or
            self.stage == 3 
            )
    
        self.is_eq = (
            self.stage == 4 or
            self.stage == 5 or
            self.stage == 6 or
            self.stage == 7 or
            self.stage == 8 
            )
        
        
        
        
    def continue_sim(self):
        
        # Defaults
        bin_coordinates     = ""
        extended_system     = ""
        velocities          = ""
        
        if(self.stage!=0):                                                                              # If not Initializing Simulation
            input           = NamdConf.SIM_NAME_STR_ARRAY[self.stage-1]                                          # Get the previous simulation step's id
            bin_coordinates = "{0:<25.25} {1}.coor\n".format( "BinCoordinates " , input )               # 
            extended_system = "{0:<25.25} {1}.xsc \n".format( "ExtendedSystem " , input )               # 
            if(not self.dis_temp):                                                                      # 
                velocities  = "{0:<25.25} {1}.vel \n".format( "BinVelocities "  , input )               # 
        elif(self.is_restart):                                                                          # 
            input           = NamdConf.SIM_NAME_STR_ARRAY[self.stage]                                            # 
            bin_coordinates = "{0:<25.25} {1}.coor\n".format( "BinCoordinates " , input )               # 
            extended_system = "{0:<25.25} {1}.xsc \n".format( "ExtendedSystem " , input )               # 
            velocities      = "{0:<25.25} {1}.vel \n".format( "BinVelocities "  , input )               # 
        
        return "\n"+bin_coordinates + extended_system + velocities+"\n"
    
    def get_settings(self):
        settings = "\n"
        if( self.md == NamdConf.AMBER):                                                         # Amber
            settings =             "{0:<25.25} {1}\n".format( "amber"             , "on"   )        # 
            settings = settings +  "{0:<25.25} {1}\n".format( "readexclusions"    , "yes"  )        # 
            settings = settings +  "{0:<25.25} {1}\n".format( "ambercoor"         , self.coords )   # Amber Coordinates
            settings = settings +  "{0:<25.25} {1}\n".format( "parmfile"          , self.parm   )   # Amber Parameters
        elif( self.md == NamdConf.CHARMM):                                                      # Charmm
            settings     =            "{0:<25.25} {1}\n".format( "paraTypeCharmm" , "on" )          # 
            settings     = settings + "{0:<25.25} {1}\n".format( "coordinates"    , self.coords )   # Charmm Coordinates
            settings     = settings + "{0:<25.25} {1}\n".format( "structure"      , self.parm   )   # Charmm Structure
            for toppar in NamdConf.TOPPAR_ARRAY:                                                    #
                settings = settings + "{0:<25.25} {1}\n".format( "parameters"     , toppar )        # Charmm Parameters
        
        return settings
    
    def force_field_parameters(self):
        ff_parm = "\n# Force Field Parameters\n" 
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "exclude"        , "scaled1-4")         # 
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "1-4scaling"     , "1.0"  )             # (Seen: 1/1.2, 1.0)
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "cutoff"         , "12.0"  )            # Distance for nonbond cutoff           (Seen: 12, 14)
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "switching"      , "on"  )              # Softens potential
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "switchdist"     , "10.0"  )            # Distance for switching function       (Usually: cutoff - 2) 
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "pairlistdist"   , "16.0"  )            # Atoms move <2A pr cycle               (Usually: cutoff + 2) 
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "margin"         , "1.0"  )             # 
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "rigidBonds"     , "all"  )             # needed for 2fs steps
        ff_parm = ff_parm +  "{0:<25.25} {1}\n".format( "rigidTolerance" , "0.0005"  )          # 
        return ff_parm
    
    def cell(self,x=64,y=64,z=64):
        cell_settings = "\n# Cell Settings\n"
        if(self.init_sim):
            cell_settings = cell_settings + "{0:<25.25} {1} {2} {3}\n".format( "cellBasisVector1" , str(x), str(0), str(0)  )          # x = max(x)-min(x)
            cell_settings = cell_settings + "{0:<25.25} {1} {2} {3}\n".format( "cellBasisVector2" , str(0), str(y), str(0)  )          # y = max(y)-min(y)
            cell_settings = cell_settings + "{0:<25.25} {1} {2} {3}\n".format( "cellBasisVector3" , str(0), str(0), str(z)  )          # z = max(z)-min(z)
            cell_settings = cell_settings + "{0:<25.25} {1} {2} {3}\n".format( "cellOrigin"       , str(0), str(0), str(0)  )          # Center of Box
        # Wrap
        cell_settings = cell_settings + "{0:<25.25} {1}\n".format( "wrapWater"   , "on" )          # Wrap water to central cell 
        cell_settings = cell_settings + "{0:<25.25} {1}\n".format( "wrapAll"     , "on" )          # Wrap other molecules too 
        cell_settings = cell_settings + "{0:<25.25} {1}\n".format( "wrapNearest" , "on" )          # 
        
        return cell_settings
    
    def time(self):
        time_step = "\n# Time\n"
        time_step = time_step + "{0:<25.25} {1}\n".format( "firsttimestep"      , str(self.first_time_step))    # 
        if(self.heating):                                                                                       #
            time_step = time_step + "{0:<25.25} {1}\n".format( "timestep"       , str(1.0))                     # 
        else:                                                                                                   #
            time_step = time_step + "{0:<25.25} {1}\n".format( "timestep"       , str(2.0))                     # 
        time_step = time_step + "{0:<25.25} {1}\n".format( "stepspercycle"      , str(10) )                     # 
        time_step = time_step + "{0:<25.25} {1}\n".format( "nonbondedFreq"      , str(1)  )                     # 
        time_step = time_step + "{0:<25.25} {1}\n".format( "fullElectFrequency" , str(2)  )                     # 
        return time_step

    def pme(self,*args):
        particle_mesh_ewald = "\n# Particle Mesh Ewald\n" 
        if(not self.is_min):
            particle_mesh_ewald = particle_mesh_ewald + "{0:<25.25} {1}\n".format( "PME"            , "yes"  )                     #  Particle Mesh Ewald (for periodic electrostatics)
            particle_mesh_ewald = particle_mesh_ewald + "{0:<25.25} {1}\n".format( "PMEGridSpacing" , str(1.0)  )                  # 
            #particle_mesh_ewald = particle_mesh_ewald + "{0:<25.25} {1}\n".format( "PMEInterpOrder" , str(6)  )                    # interpolation order (spline order 6 in charmm)
            #if(len(args) == 3)
            #    PMEGridSizeX           args           ;# Replace PMEXX 
            #    PMEGridSizeY           args           ;# Replace PMEYY
            #    PMEGridSizeZ           args           ;# Replace PMEZZ
        return particle_mesh_ewald
        
    def temperature(self):
        temperature = "\n# Temperature\n"
        if(self.init_sim):
            temperature = temperature + "{0:<25.25} {1}\n".format( "temperature"      , str(0)  )                   # 
        elif(self.dis_temp):
            temperature = temperature + "{0:<25.25} {1}\n".format( "temperature"      , str(self.temperature)  )    # 
        if(not self.is_min):
            temperature = temperature + "{0:<25.25} {1}\n".format( "langevin"         , "on"  )                     # 
            temperature = temperature + "{0:<25.25} {1}\n".format( "langevinDamping"  , str(1)  )                   # 
            temperature = temperature + "{0:<25.25} {1}\n".format( "langevinTemp"     , str(self.temperature)  )    # 
            temperature = temperature + "{0:<25.25} {1}\n".format( "langevinHydrogen" , "off"  )                    # 
        return temperature
    
    def pressure(self):
        pressure = "\n#Pressure\n"
        pressure = pressure + "{0:<25.25} {1}\n".format( "useGroupPressure"     , "yes"  )                  # needed for 2fs steps
        pressure = pressure + "{0:<25.25} {1}\n".format( "useFlexibleCell"      , "no"  )                   # no for water box, yes for membrane
        pressure = pressure + "{0:<25.25} {1}\n".format( "useConstantArea"      , "no"  )                   # no for water box, yes for membrane
        pressure = pressure + "{0:<25.25} {1}\n".format( "langevinPiston"       , "on"  )                   # 
        pressure = pressure + "{0:<25.25} {1}\n".format( "langevinPistonTarget" , str(1.01325)  )           # in bar -> 1 atm
        pressure = pressure + "{0:<25.25} {1}\n".format( "langevinPistonPeriod" , str(100.0)  )             # 
        pressure = pressure + "{0:<25.25} {1}\n".format( "langevinPistonDecay"  , str(50.0)  )              # 
        pressure = pressure + "{0:<25.25} {1}\n".format( "langevinPistonTemp"   , str(self.temperature)  )  # 
        return pressure
    
    def constraints(self,file_str,harmonic=False,scaling=1.0):
        constraints = "\n#Constraints\n"
        
        if(harmonic):
            constraints = constraints + "{0:<25.25} {1}\n".format( "constraints"        , "on"  )
            constraints = constraints + "{0:<25.25} {1}\n".format( "consRef"            , file_str  )
            constraints = constraints + "{0:<25.25} {1}\n".format( "consKFile"          , file_str  )
            constraints = constraints + "{0:<25.25} {1}\n".format( "consKCol"           , "B"  )
            constraints = constraints + "{0:<25.25} {1}\n".format( "constraintScaling"  , str(scaling)  )
        else:
            constraints = constraints + "{0:<25.25} {1}\n".format( "fixedAtoms"     , "on"  )
            constraints = constraints + "{0:<25.25} {1}\n".format( "fixedAtomsCol"  , "B"   )
            constraints = constraints + "{0:<25.25} {1}\n".format( "fixedAtomsFile" , file_str   )
        
        return constraints
    
    def output(self):
        output_name = NamdConf.SIM_NAME_STR_ARRAY[self.stage]
        output="\n# Output\n"
        output = output + "{0:<25.25} {1}\n".format( "binaryoutput"   , "yes"  )                    # 
        output = output + "{0:<25.25} {1}\n".format( "outputTiming"   , str(50)  )                  # 
        output = output + "{0:<25.25} {1}\n".format( "xstFile"        , output_name+".xst"  )       # 
        output = output + "{0:<25.25} {1}\n".format( "outputname"     , output_name  )              # 
        output = output + "{0:<25.25} {1}\n".format( "dcdfile"        , output_name+".dcd"  )       # 
        output = output + "{0:<25.25} {1}\n".format( "restartname"    , output_name+".restart"  )   # 
        output = output + "\n # Output Frequency\n"
        if(self.is_min):
            output = output + "{0:<25.25} {1}\n".format( "restartfreq"      , str(500)  )           # 
            output = output + "{0:<25.25} {1}\n".format( "dcdfreq"          , str(500)  )           # 
            output = output + "{0:<25.25} {1}\n".format( "xstFreq"          , str(500)  )           # 
            output = output + "{0:<25.25} {1}\n".format( "outputEnergies"   , str(500)  )           # 
            output = output + "{0:<25.25} {1}\n".format( "outputPressure"   , str(500)  )           # 
        else: 
            output = output + "{0:<25.25} {1}\n".format( "restartfreq"      , str(5000)  )          # 
            output = output + "{0:<25.25} {1}\n".format( "dcdfreq"          , str(5000)  )          # 
            output = output + "{0:<25.25} {1}\n".format( "xstFreq"          , str(5000)  )          # 
            output = output + "{0:<25.25} {1}\n".format( "outputEnergies"   , str(5000)  )          # 
            output = output + "{0:<25.25} {1}\n".format( "outputPressure"   , str(5000)  )          # 
        return output
    
    def run(self):
        output = "\n# Run\n"
        if(self.is_min):
            output = output + "{0:<25.25} {1}\n".format( "minimization"         , "on"  )              # 
            output = output + "{0:<25.25} {1}\n".format( "minimize"             , str(10000)  )        # 
        elif(self.is_eq):
            if(self.heating):
                output = output + "{0:<25.25} {1}\n".format( "numsteps"         , str(250000)  )        # 
            else:
                output = output + "{0:<25.25} {1}\n".format( "numsteps"         , str(125000)  )        # 
        else:
            output = output + "{0:<25.25} {1}\n".format( "run"                  , str(150000000)  )        # 
        return output
        
    
    def make_conf_file(self):
        conf = open(NamdConf.SIM_NAME_STR_ARRAY[self.stage]+".conf","w+")
        conf.write(NamdConf.continue_sim(self))
        conf.write(NamdConf.get_settings(self))
        conf.write(NamdConf.force_field_parameters(self))
        conf.write(NamdConf.cell(self))
        conf.write(NamdConf.time(self))
        conf.write(NamdConf.pme(self))
        conf.write(NamdConf.temperature(self))
        if(not self.is_min):
            conf.write(NamdConf.pressure(self))
        if( self.stage == 0 ):
            conf.write(NamdConf.constraints(self,"h_free.pdb"))
        elif( self.stage == 1 ):
            conf.write(NamdConf.constraints(self,"h_h2o_free.pdb"))
        elif( self.stage == 2 ):
            conf.write(NamdConf.constraints(self,"h_h2o_r_free.pdb"))
        elif( self.stage == 4 ):
            conf.write(NamdConf.constraints(self,"not_backbone_free.pdb",True,1.0))
        elif( self.stage == 5 ):
            conf.write(NamdConf.constraints(self,"not_backbone_free.pdb",True,0.75))
        elif( self.stage == 6 ):
            conf.write(NamdConf.constraints(self,"not_backbone_free.pdb",True,0.50))
        elif( self.stage == 7 ):
            conf.write(NamdConf.constraints(self,"not_backbone_free.pdb",True,0.25))
        
        conf.write(NamdConf.output(self))
        conf.write(NamdConf.run(self))
        
        conf.close()
        
    

    







def rot_xyz(pdb_path,i):
    #                0       1       2       3      4      5      6      7      8       9
    #str_array = ["min_1","min_2","min_3","min_4","eq_1","eq_2","eq_3","eq_4","eq_5","prod"]
    
    
    is_restart      = False         # 
    production      = False         # Production: Proper Temperature On, No Constraints
    temperature     = 300
    first_time_step = 0
    # Molecular Dynamics Engines 
    is_charmm      = True
    is_amber       = False
    
    
    
    discontinuous_temperature= (
        i==4 or 
        i==9
        )
    
    init_sim = (
        i==0 and 
        not is_restart
        )
    heating = (
        i==4
        )
    
    # Defaults
    
    
    ####################
    ## Input Settings ##
    ####################
    
    
    settings = ""
    if(is_charmm):                                  # Charmm
        settings = charmm_settings(coords,parm)     #
    elif(is_amber):                                 # Amber
        settings = amber_settings(coords,parm)      #
    
    
    
    
    

if (__name__ == "__main__"):
    a = NamdConf(int(sys.argv[1]))
    a.make_conf_file()
    

