# Set Your Variables!                                         # User Actions
set in_name 4_protein
set out_name 5_protein

# Load Files
mol new ${in_name}.psf
mol addfile ${in_name}.pdb


# Import Packages
package require psfgen
package require solvate
package require autoionize


# Solvate 15A Padding
#solvate ${in_name}.psf ${in_name}.pdb -t 15 -o ${out_name}_temp
# Solvate 64A Box
solvate ${in_name}.psf ${in_name}.pdb -minmax {{-32 -32 -32} {32 32 32}} -o ${out_name}_temp


# Ionize 15A Padding
#autoionize -psf ${out_name}_temp.psf -pdb ${out_name}_temp.pdb -neutralize -cation SOD -o ${out_name}
# Ionize 64A Box
autoionize -psf ${out_name}_temp.psf -pdb ${out_name}_temp.pdb -neutralize -cation SOD -o ${out_name}



# Calculate center and size
set all [atomselect top all]
set center [measure center $all]
set M [measure minmax $all]
set size [vecsub [lindex $M 1] [lindex $M 0]]

# Save that to a file
set outfile [open "dimens.txt" w]
puts $outfile $center
puts $outfile $size
close $outfile

# Exit
quit
