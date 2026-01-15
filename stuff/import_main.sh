    #!/bin/bash
    dataset="../../dataset/SCHAEFFER/"

    harmsus=("HarmSus" "Harmonic sound" "Sinsoidal sound" "Flat sustain")
    harmimp=("HarmImp" "Harmonic sound" "Sinsoidal sound" "Impulse")
    harmiter=("HarmIter" "Harmonic sound" "Sinusoidal sound" "Iteration" "Regular pulse train")
    
    noisesus=("NoiseSus" "Noisy sound" "Noise" "Flat sustain")
    noiseimp=("NoiseImp" "Noisy sound" "Noise" "Impulse")
    noiseiter=("NoiseIter" "Noisy sound" "Noise" "Flat sustain"  "Regular pulse train")
    
    vacillatingsus=("CompositeSus" "Composite or Stratified sound" "Vacillating sustain" "Flat sustain")
    compositeimp=("CompositeImp" "Vacillating sustain" "Composite or Stratified sound" "Impulse")
    compositeiter=("CompositeIter" "Vacillating sustain" "Composite or Stratified sound" "Regular pulse train" "Iteration")
    base="../classification/training_data"


    echo $base/${harmsus[0]}
    # echo "Clearing directories...\n"
    # for directory in keyA keyB keyC keyD keyE keyF keyG keyH keyI
    # do
    #     rm -rf $d/*.wav
    # done

    echo "Copying files from dataset...\n\n"
    for d in "$dataset"*/; do
        for j in "$d"*.json; do
            if test -f "$j"
            then
  #  	    
  #  	      ##############################
  #  	        # Harmonic sustain
  #  	        if [ ! -d "$base/${harmsus[0]}" ]; then
  #  	            mkdir "$base/${harmsus[0]}"
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmsus[1]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${harmsus[3]} ]]; then
  #  	            #  		echo "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmsus[0]}
  #  	        fi
  #  	        # Harmonic sustain (Sinusoidal)
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmsus[2]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${harmsus[3]} ]]; then
  #  	            # echo "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmsus[0]}
  #  	        fi
  #  	        ##############################
  #  	        # Harmonic impulse
  #  	        if [ ! -d "$base/${harmimp[0]}" ]; then
  #  	            mkdir "$base/${harmimp[0]}"
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmimp[1]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${harmimp[3]} ]]; then
  #  	            #        		echo "HarmImp" "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmimp[0]}
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmimp[2]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${harmimp[3]} ]]; then
  #  	            # echo "HarmImp" "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmimp[0]}
  #  	        fi
  #  	        ##############################
  #  	        # Harmonic iteration
  #  	        if [ ! -d "$base/${harmiter[0]}" ]; then
  #  	            mkdir "$base/${harmiter[0]}"
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmiter[1]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${harmiter[3]} ]]; then
  #  	    
  #  	            # echo "Harmiter0" "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmiter[0]}
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmiter[2]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${harmiter[3]} ]]; then
  #  	            # echo "HarmIter1" "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmiter[0]}
  #  	        fi
  #  	        if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${harmiter[1]} ]] &&
  #  	        	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${harmiter[4]} ]]; then
  #  	            # echo "HarmIter2" "$d""`cat "$j" | jq -r '.object.filename'`"
  #  	            cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${harmiter[0]}
  #  	        fi
  #   	      ##############################
  #   	      # Noise sustain
  #   	      if [ ! -d "$base/${noisesus[0]}" ]; then
  #   	          mkdir "$base/${noisesus[0]}"
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${noisesus[1]} ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${noisesus[3]} ]]; then
  #   	          # echo "Noisesus0" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noisesus[0]}
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels.type')" == *${noisesus[2]}* ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${noisesus[3]} ]]; then
  #   	          # echo "Noisesus1" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noisesus[0]}
  #   	      fi
  #   	      ##############################
  #   	      # Noise impulse
  #   	      if [ ! -d "$base/${noiseimp[0]}" ]; then
  #   	          mkdir "$base/${noiseimp[0]}"
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${noiseimp[1]} ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${noiseimp[3]} ]]; then
  #   	          # echo "Noiseimp0" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noiseimp[0]}
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels.type')" == *${noiseimp[2]}* ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${noiseimp[3]} ]]; then
  #   	          # echo "Noiseimp1" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noiseimp[0]}
  #   	      fi
  #   	      ##############################
  #   	      # Noise iteration
  #   	      if [ ! -d "$base/${noiseiter[0]}" ]; then
  #   	          mkdir "$base/${noiseiter[0]}"
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${noiseiter[1]} ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${noiseiter[3]} ]]; then
  #   	          # echo "Noiseiter0" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noiseiter[0]}
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels.type')" == *${noiseiter[2]}* ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${noiseiter[3]} ]]; then
  #   	          # echo "Noiseiter1" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noiseiter[0]}
  #   	      fi
  #   	      if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${noiseiter[1]} ]] &&
  #   	          	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${noiseiter[4]} ]]; then
  #   	          # echo "Noiseiter2" "$d""`cat "$j" | jq -r '.object.filename'`"
  #   	          cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${noiseiter[0]}
  #   	      fi
                 ##############################
                 # Noise sustain
                 if [ ! -d "$base/${vacillatingsus[0]}" ]; then
                     mkdir "$base/${vacillatingsus[0]}"
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == ${vacillatingsus[1]} ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${vacillatingsus[3]} ]]; then
                     # echo "Vacillatingsus0" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${vacillatingsus[0]}
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == *${vacillatingsus[1]}* ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${vacillatingsus[2]} ]]; then
                     # echo "Vacillatingsus1" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${vacillatingsus[0]}
                 fi
                 ##############################
                 # Noise impulse
                 if [ ! -d "$base/${compositeimp[0]}" ]; then
                     mkdir "$base/${compositeimp[0]}"
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${compositeimp[1]} ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${compositeimp[3]} ]]; then
                     # echo "Compositeimp0" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${compositeimp[0]}
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == *${compositeimp[2]}* ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${compositeimp[3]} ]]; then
                     # echo "Compositeimp1" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${compositeimp[0]}
                 fi
                 ##############################
                 # Noise iteration
                 if [ ! -d "$base/${compositeiter[0]}" ]; then
                     mkdir "$base/${compositeiter[0]}"
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${compositeiter[1]} ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${compositeiter[4]} ]]; then
                     # echo "Compositeiter0" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${compositeiter[0]}
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels."mass-type"')" == *${compositeiter[2]}* ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${compositeiter[3]} ]]; then
                     # echo "Compositeiter1" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${compositeiter[0]}
                 fi
                 if  [[ "$(cat "$j" | jq -r '.object.labels.sustain')" == ${compositeiter[1]} ]] &&
                     	[[ "$(cat "$j" | jq -r '.object.labels."pulse-typology"')" == ${compositeiter[3]} ]]; then
                     # echo "Compositeiter2" "$d""`cat "$j" | jq -r '.object.filename'`"
                     cp "$d""`cat "$j" | jq -r '.object.filename'`" $base/${compositeiter[0]}
                 fi
               
            fi
        done
    done

    echo "Done!\n"
