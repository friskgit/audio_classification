#!/bin/bash
dataset="../../dataset/SCHAEFFER/"
keyA=Impulse
keyB=Iteration
base="../classification/training_data/"
dirA="$base""$keyA"
dirB="$base""$keyB"

echo "Clearing directories...\n\n"
rm -rf $dirB/*.wav
rm -rf $dirA/*.wav

echo "Copying files from dataset...\n\n"
for d in "$dataset"*/; do
    for j in "$d"*.json; do
	if test -f "$j"
	then
	    if [[ "$(cat "$j" | jq '.object.labels.sustain')" == "\""$keyB"\"" ]]; then
		if [ ! -d "$dirB" ]; then
		    mkdir "$dirB"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$dirB"
	    fi
	    if [[ "$(cat "$j" | jq '.object.labels."pulse-typology"')" == "\""$keyA"\"" ]]; then
		if [ ! -d "$dirA" ]; then
		    mkdir "$dirA"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$dirA"
	    fi
	fi
    done
done

echo "Done!\n"

#!/bin/bash
dataset="../../dataset/SCHAEFFER/"
keyA="Vacillating sustain"
keyB="Flat sustain"
base="../classification/training_data/"
dirA="$base""$keyA"
dirB="$base""$keyB"
path=".object.labels.sustain"

echo "Clearing directories...\n\n"
if [ ! -d "$dirB" ]; then
   rm -rf $dirB/*.wav
fi
if [ ! -d "$dirA" ]; then
    rm -rf $dirA/*.wav
fi

echo "Copying files from dataset...\n\n"
for d in "$dataset"*/; do
    for j in "$d"*.json; do
	if test -f "$j"
	then
	    if [[ "$(cat "$j" | jq $path)" == "\""$keyA"\"" ]]; then
		if [ ! -d "$dirA" ]; then
		    mkdir "$dirA"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$dirA"
	    fi
	    if [[ "$(cat "$j" | jq $path)" == "\""$keyB"\"" ]]; then
		if [ ! -d "$dirB" ]; then
		    mkdir "$dirB"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$dirB"
	    fi
	fi
    done
done

echo "Done!\n"
