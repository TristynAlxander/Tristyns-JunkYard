# Set Your Variables!                                         # User Actions
set in_name 2_protein
set out_name 3_protein


# Import Packages
package require psfgen

# Load Topologies                                             # User Actions
topology toppar/top_all36_prot.rtf

# Rename "Misnomers"
pdbalias residue HIS HSE
pdbalias atom ILE CD1 CD

# Select Segment
segment SEG {pdb ${in_name}.pdb}

# Get Coordinates
#regenerate angles dihedrals                                   #  Comment out "AUTO ANGLES DIHE PATCH" in topology file
coordpdb ${in_name}.pdb SEG
guesscoord



# Write Outputs
writepdb ${out_name}.pdb
writepsf ${out_name}.psf

#Exit
quit
