#!/bin/bash

pulset=Impulse
sustain=Iteration
base="/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/classification/training_data/"
imp="$base""$pulset"
iter="$base""$sustain"

echo "Clearing directories...\n\n"
rm -rf $iter/*.wav
rm -rf $imp/*.wav

echo "Copying files from dataset...\n\n"
for d in */; do
    for j in "$d"*.json; do
	if test -f "$j"
	then
	    if [[ "$(cat "$j" | jq '.object.labels.sustain')" == "\""$sustain"\"" ]]; then
		if [ ! -d "$iter" ]; then
		    mkdir "$iter"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$iter"
	    fi
	    if [[ "$(cat "$j" | jq '.object.labels."pulse-typology"')" == "\""$pulset"\"" ]]; then
		if [ ! -d "$imp" ]; then
		    mkdir "$imp"
		fi
		cp "$d""`cat "$j" | jq -r '.object.filename'`" "$imp"
	    fi
	fi
    done
done

echo "Done!\n"
