#!/bin/bash

read -p "Please enter your S3 bucket name: " bucketname

read -p "Do you want to upload the Github data to S3? (y/n) " gh_answer

case $gh_answer in

    [yY] )
        aws s3 cp "./data/github/clean/gh_clean.csv" "s3://$bucketname/gh_clean.csv"
        echo "copied the clean Github data to your bucket $bucketname "
        ;;
    [nN] )
        echo "Not uploading the Github data."
        ;;
    esac

read -p "Do you want to upload the LibIo data to S3? (y/n) " lib_answer 

case $lib_answer in
    [yY] )
        read -p "Do you want to upload all files? (y/n) " lib_all_answer 

        case $lib_all_answer in
            [yY] )
                aws s3 sync "./data/libcsv/clean/" "s3://$bucketname/"  
                echo "Uploaded all clean lib files to your bucket $bucketname "
                ;;
            [nN] )
                read -p "Do you want to upload just one file? (y/n) " lib_single_answer 
                case $lib_single_answer in
                    [yY] )
                        read -p "What is the file called you want to upload? (Standard: clean_<xx>)" lib_file 
                        echo "File $lib_file is getting uploaded to s3."
                        aws s3 cp "./data/libcsv/clean/$lib_file.csv" "s3://$bucketname/$lib_file.csv" 
                        ;;
                    [nN] )
                        echo "Not uploading anything from the libio files."
                        ;;
                    esac
                ;;
        esac
        ;;
    [nN] )
        read -p "Not uploading anything from the libio data."
        ;;
    esac

