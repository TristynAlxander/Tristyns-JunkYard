# Set Your Variables!                                         # User Actions
set in_name 1_protein
set out_name 2_protein

# Load File
mol addfile ${in_name}.pdb

# Selects Protein
set my_mol [atomselect top protein]

# Reformat File 
$my_mol writepdb ${out_name}.pdb

#Exit
quit
