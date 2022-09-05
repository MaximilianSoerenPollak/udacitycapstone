#!/bin/bash


read -p "Do you want to check the data quality of the Github Data? (y/n) " answer1


case $answer1 in

    [yY] )
            echo "Checking Github Data quality..."
            python g_e_github.py
            ;;
    [nN] )
            echo "Not checking Github Data quality. Moving on."
            ;;
    esac 
read -p "Do you want to check the data quality of the Libio Data? (y/n) " answer2

case $answer2 in

    [yY] )
        read -p "Do you want to check all csv's? (y/n) || Note: This can take a really long time. " answer3

            case $answer3 in

                [yY] )
                    read -p "Do you want to save the reports in a file? (y/n) " report 

                    case $report in 

                        [yY] )
                            if [ -f dataqualityreport.txt ] 
                            then 
                                read -p "'Dataqualitreport' file already exists. Do you want to append the new report? (y/n) " append
                                case $append in
                                    [yY] )
                                        now=$(date +"%T")
                                        insert="---------NEW REPORT FROM $now STARTING HERE----------"
                                        echo $insert >> dataqualityreport.txt
                                        ;;
                                    [nN] )
                                        echo "Removing dataqualityreport.txt. Please confirm"

                                        rm -i "dataqualityreport.txt"
                                    ;;
                                esac 
                            fi 
                            echo "Saving reports to 'dataqualityreport.txt' " 
                            counter=0
                            for file in data/libcsv/clean/*.csv;
                            do
                                if [ -f "$file" ]
                                then
                                    python g_e_libio.py $counter >> dataqualityreport.txt  
                                    counter=$((counter + 1))
                                else
                                    echo "Warning there was a problem with checking $file"
                                fi
                            done
                            echo "Checked all Files for Data quality"
                            ;;
                        [nN] )
                            echo "Not saving report to a file."
                            counter=0
                            for file in data/libcsv/raw/*.csv;
                            do
                                if [ -f "$file" ]
                                then
                                    python g_e_libio.py $counter 
                                    counter=$((counter + 1))
                                else
                                    echo "Warning there was a problem with checking $file"
                                fi
                            done
                            echo "Checked all Files for Data quality"
                            ;;
                    esac
                    ;;
                [nN] )
                read -p "Do you want to check one of the csv's ? (y/n) " answer4
                        
                        case $answer4 in
                            
                            [yY] )
                                read -p "Please enter the number of the csv you want to check. (0-xx) " csvfile 
                                python g_e_libio.py "$csvfile"
                                
                                echo "-----Data Quality Check Completed----"
                                ;;

                            [nN] )
                                echo "Not checking the data quality. "
                                ;;
                        esac
                ;;
                esac
        ;;
        [nN] )
                echo "Moving on" 
                ;;
    esac
