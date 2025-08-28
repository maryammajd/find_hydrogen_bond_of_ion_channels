# This bash file finds all the hydrogen bonds that are made during the given simulation 
if [ $# -lt 1 ]; then
	echo \"Usage:\"
	echo \"1.find_dist.sh directory_of_models \(tpr and xtc files needed with the same name\; provide the file names without suffix \)\"
	exit 1
fi


SOURCEFILE=$1
OUTPUTDIR="outputs"


if [ ! -d $OUTPUTDIR ]
then
  mkdir $OUTPUTDIR || exit
fi


HELIX=$(seq 0 1 8)
mapfile -t INDEX_FILES < <(find inputs -type f -name "*.ndx" -exec basename {} .ndx \;)

for helix1 in $HELIX
do
    for helix2 in $HELIX
    do
        if [[ "$helix1" != "$helix2" ]];
        then
        for INDEX_FILE in "${INDEX_FILES[@]}"
        do 
            # echo $INDEX_FILE
            echo -e "$helix1 \n $helix2" | gmx hbond -f "$SOURCEFILE".xtc -s "$SOURCEFILE".tpr -n inputs/$INDEX_FILE.ndx -o $OUTPUTDIR/$INDEX_FILE-$helix1-$helix2 -num $OUTPUTDIR/$INDEX_FILE-$helix1-$helix2 -dist $OUTPUTDIR/$INDEX_FILE-$helix1-$helix2-dist
        done
        fi
    done 
done
