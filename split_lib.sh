#!/bin/bash

read -p "Do you have the 'lib_repo.csv' in the '/data/libcsv/' folder? (y/n) " right_place



case $right_place in
    [yY] )
        read -p "Do you want to splitt the csv in equal parts now? (y/n) " split_csv
        case $split_csv in
            [yY] )
                echo "Splitting csv in equal parts."
                echo "All CSV's will be put into '/data/libcsv/raw'."
                head -n 100 ./data/libcsv/lib_repo.csv > ./data/libcsv/lib_repo_reduced.csv
                split -l 1000000 ./data/libcsv/lib_repo.csv ./data/libcsv/raw/split_ --additional-suffix=.csv
                ;;
            [nN] )
                echo "Not splitting the csv, ending script."
                ;;
        esac
        ;;   
    [nN] )
        echo "Please put the csv in the right place '/data/libcsv/' and run this script again."
        ;;
    esac
