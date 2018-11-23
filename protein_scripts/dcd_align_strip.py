# Imports
import MDAnalysis
from MDAnalysis.analysis import align

# Imports for Main
if (__name__ == "__main__"):
    import sys
    import os


def save_dcd(uni,dcd_out=None, sel_str="not segid SOLV",stride=100):
    if(out_name == None):
        dcd_out = dcd_in[:-4]+"_new.dcd"
    sel = uni.select_atoms(sel_str)                                                         # Make Selection
    with MDAnalysis.Writer(dcd_out, n_atoms=sel.n_atoms) as W:                              # Make Writer
        for i,ts in zip(range(0,len(uni.trajectory)),uni.trajectory):                       # For Timestep
            if(i%stride == 0):                                                              # with index matching stride
                W.write(sel)                                                                # Save Selected

def align_traj(traj_uni, ref_uni, sel_str="name CA"):
    sel_ref = ref_uni.select_atoms(sel_str)                                         # 
    alignment = align.AlignTraj(traj_uni, ref_uni, in_memory=False, select=sel_str)
    alignment.run()
    return traj_uni

if (__name__ == "__main__"):
    sel_str="not segid SOLV"
    
    # sys.argv[0] is this script, so don't count it.
    if(len(sys.argv) == 2):
        pdb      = os.path.abspath(sys.argv[1])             # 
        path     = os.path.dirname(pdb)+"/"                 # 
        new_pdb  = sys.argv[2][:-4]+"_new.pdb"              # 
        
        traj_uni = MDAnalysis.Universe(pdb)                 # 
        sel = traj_uni.select_atoms(sel_str).write(new_pdb) # 
        ref_uni  = MDAnalysis.Universe(path+new_pdb)        # 
    elif(len(sys.argv) == 3):
        psf  = os.path.abspath(sys.argv[1])                 # 
        dcd  = os.path.abspath(sys.argv[2])                 # 
        path = os.path.dirname(dcd)+"/"                     # 
        pdb  = sys.argv[2][:-4]+"_new.pdb"                  # 
        
        traj_uni = MDAnalysis.Universe(psf, dcd)            # 
        sel = traj_uni.select_atoms(sel_str).write(pdb)     # 
        ref_uni  = MDAnalysis.Universe(path+pdb)            # 
    elif(len(sys.argv) == 4):
        psf      = os.path.abspath(sys.argv[1])             # 
        dcd      = os.path.abspath(sys.argv[2])             # 
        pdb_ref  = os.path.abspath(sys.argv[3])             # 
        
        traj_uni = MDAnalysis.Universe(psf, dcd)            # 
        ref_uni  = MDAnalysis.Universe(pdb_ref)             # 
        traj_uni = align_traj(traj_uni,ref_uni)             # 
    else:
        psf = "5fo5_ion.psf"
        dcd = "5fo5_ion-0.dcd"
        pdb_ref = "5fo5_ion.pdb"
        
        traj_uni = MDAnalysis.Universe(psf, dcd)            # 
        ref_uni  = MDAnalysis.Universe(pdb_ref)             # 
        traj_uni = align_traj(traj_uni,ref_uni)             # 
    
    
    traj_uni = align_traj(traj_uni,ref_uni)
    
    save_dcd(traj_uni, dcd_out=sys.argv[2],sel_str=sel_str)

