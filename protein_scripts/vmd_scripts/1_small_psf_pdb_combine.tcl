package require psfgen

set in_protein  3_protein
set in_small_m  small_molecule_final
set out_system  4_protein

readpsf  ${in_protein}.psf
readpsf  ${in_small_m}.psf

coordpdb ${in_protein}.pdb
coordpdb ${in_small_m}.pdb

writepsf ${out_system}.psf
writepdb ${out_system}.pdb

# Exit
quit 