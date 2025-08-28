# This bash file finds the distance of the given residues in the $INDEX_FILE at each timepoint for the given simulation. 
if [ $# -lt 1 ]; then
	echo \"Usage:\"
	echo \"1.find_dist.sh directory_of_models \(tpr and xtc files needed with the same name\; provide the file names without suffix \)\" 
	exit 1
fi


OUTPUTDIR="outputs"
SOURCEFILE=$1
mapfile -t INDEX_FILES < <(find inputs -type f -name "*.ndx" -exec basename {} .ndx \;)


for vsd in "${INDEX_FILES[@]}";
do 
INDEX_FILE="$OUTPUTDIR/H-bond_pairs_"$vsd".ndx"
m=$(grep -c "\[" $INDEX_FILE)  # Define m as a number

echo -e "$(seq 0 "$((m-1))" | tr 'n' ' ')" | gmx distance -n $INDEX_FILE  -f "$SOURCEFILE".xtc -s "$SOURCEFILE".tpr -oall $OUTPUTDIR/"${SOURCEFILE##*/}"-dist-all-$vsd
done
