#!/bin/bash

echo "Welcome. This script will guide you through the whole process of running this project."

# ----------LibIO-------------------
echo "Starting LibIO data script."
sh split_lib.sh
sh lib_cleaning.sh 
echo "Finished with LibIO data scripts."

# ---------- Github ------------
echo "Starting Github data scripts."
read -p "Do you want to collect the Github data from the API and clean it? Note: This can take a while. (y/n) " collect_gh_data 

case $collect_gh_data in
    [yY] )
        echo "Starting data collection from Github API."
        python data_acquisition.py 
        python github_clean.py 
    ;;
    [nN] )
        echo "Skipping data collection from Github."
    ;;
esac
echo "Finished with Github data scripts."

# ---------- Data QUalaity -------------
echo "Starting quality check scripts."
sh quality_check.sh
echo "Finished quality check scripts."

# --------AWS----------- 
echo "Starting AWS scripts."

read -p "Do you want to start all AWS services? (y/n) " start_aws 

case $start_aws in 
    [yY] )
        echo "Starting AWS services."
        python aws_startup.py
        ;;
    [nN] )
        echo "Not starting AWS services. Skipping this step."
        ;;
esac 

read -p "Do you want to upload the files to S3? (y/n) " upload_to_s3

case $upload_to_s3 in 
    [yY] )
        echo "Starting upload to S3 script."
        sh file_to_s3.sh
        ;;
    [nN] )
        echo "Not uploading files. Skipping this step."
        ;;
esac

read -p "Do you want to drop the old Redshift tables? (y/n) " drop_tables 
read -p "Do you want to load the Data into Redshift? (y/n) " load_data 
echo "Starting ETL script." 

python etl.py $drop_tables $load_data 

echo "Done with the ETL script."

echo "Done with all scripts. You are at the end of the guided script. Please verify that all your data is in the Redshift tables in your cluster."

