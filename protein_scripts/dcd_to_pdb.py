#!/usr/bin/env python
import MDAnalysis
import os
import sys

# Load Files
psf    = os.path.abspath(sys.argv[1])          # 
dcd    = os.path.abspath(sys.argv[2])          #

universe  = MDAnalysis.Universe( psf, dcd )

with MDAnalysis.Writer('seg.pdb', multiframe=True, bonds=None, n_atoms=2) as PDB:
    a = universe.select_atoms('all')
    for ts in universe.trajectory:
        PDB.write(a.atoms)
    