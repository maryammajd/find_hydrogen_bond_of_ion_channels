# this bash file creates an index file for all the formed hydrogen bonds that are created in the simulation given at step 1. This code cannot be run separately and needs the files that are created in step 1.

#!/bin/bash

OUTPUTDIR="outputs"
mapfile -t INDEX_FILES < <(find inputs -type f -name "*.ndx" -exec basename {} .ndx \;)
# Loop through all files in the current directory
for vsd in "${INDEX_FILES[@]}";
do 
for file in $OUTPUTDIR/$vsd-*.ndx; do
    # Read the file line by line
    inside_hbond_section=false
    declare -A sections
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Check if a new section starts
        if [[ "$line" =~ \[.*\] ]]; then
            # If it is an hbond section, mark it as true, otherwise false
            if [[ "$line" =~ hbond ]]; then

                inside_hbond_section=true
            else
                inside_hbond_section=false
            fi
        elif $inside_hbond_section; then
            # Extract first and third column
            read -r col1 _ col3 <<< "$line"
	    echo -e "[$col1 $col3] \n $col1 $col3" >>  "$OUTPUTDIR/H-bond_pairs_"$vsd".ndx"
            # if [[ -n "$col1" && -n "$col3" ]]; then
            #     key="${col1}-${col3}"
            #     sections["$key"]+="${col1} ${col3}"
            # fi
        fi
    # for key in "${!sections[@]}"; do
    #     echo -e "[${sections[$key]::-1}]\n"
    # done
    done < "$file"
    # # Write each section to a separate file
    # for key in "${!sections[@]}"; do
    #     echo -e "[${sections[$key]::-1}]"
    # done

done
done
