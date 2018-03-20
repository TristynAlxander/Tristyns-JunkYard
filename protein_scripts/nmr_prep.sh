pdb_file=$1
nmr_model=$2
new_file="model_"$2"_"$1
start_model=$(grep -n -e "^MODEL" $pdb_file)                                                  # Get Start Line
end_model=$(grep -n -e "^ENDMDL" $pdb_file)                                                   # Get  End  Line
start_line=$(echo $start_model | cut -d ":" -f $nmr_model )                                   # Get Start Line Number for Xth Model
end_line=$(echo $end_model | cut -d ":" -f $nmr_model )                                       # Get  End  Line Number for Xth Model
cat $pdb_file | awk "(NR > $start_line && NR < $end_line){print}" > $new_file                 # Delete Lines not between start_line and end_line    & Save
