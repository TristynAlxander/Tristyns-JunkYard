# Remake pdb with chimera
# Make mol2 with chimera
# Use cgenff
package require psfgen

set in_name small_molecule

topology  ${in_name}.str
topology  small_toppar/top_all36_cgenff.rtf
parameter toppar/par_all36_cgenff.prm

pdbalias residue HIS HSE
pdbalias atom ILE CD1 CD

segment A {pdb ${in_name}.pdb}
coordpdb ${in_name}.pdb A

guesscoord

writepdb ${in_name}_final.pdb
writepsf ${in_name}_final.psf 

#Exit
quit
