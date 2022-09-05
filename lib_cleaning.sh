#!/bin/bash
read -p "Do you want to clean the files in data/libcsv/raw/ ? (y/n) " answer 


# This variable will determin if we want to drop the columns in the cleaning or not.
drop="No"

case $answer in
    [yY] )  echo "Cleaning all files."

                        counter=0
                        for file in data/libcsv/raw/*.csv;
                        do
                            if [ -f "$file" ]
                            then
                                python lib_clean.py $file $counter $drop 
                                counter=$((counter + 1))
                                filename=$(basename $file)
                                mv $file "data/libcsv/raw/processed/$filename"
                            else
                                echo "Warning there is a problem with $file"
                            fi
                        done
                        echo "All files are processed. The script has ended."
                    ;;

    [nN] ) echo "Not cleaning Files, moving on."
        ;;  
    * ) echo "Did not recieve a valid response."
        ;;
esac
        
echo "Script finished."
