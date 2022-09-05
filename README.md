<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<h3 align="center">Udacity Nanodegree Capstone Project</h3>

  <p align="center">
    This project is my solution to the "Udacity Nanodegree in Data Engineering Capstone Project".
    This project captures a lot of data, cleans it and uploads it to AWS making it available for analysis.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<br/>
This project is an ETL pipeline that builds a Redshift cluster in AWS and then inserts data into it.
The data is gathered from the Github API as well as publicly available data from libraries.io
<br/>
This project was quite fun to make, and taught me lot about Infrastructure as code, AWS, ETL and Data Engineering in general.


#### Scoping the Project 
This project was the biggest thing I have done so far in the Data Engineering space and taught me a lot.
There were many hurdles in the finishing of it and I want to shortly describe my path to the end.  
I have decided that I want to use Github's data and some complimentary data source, since I use Github quite a bit, 
I thought it would be a good idea to use the data from it.
Gathering the data from Github is straight forward with the API they provide you have an easy and fast way to collect it.  
The complimentary data I got from libraries.io, that was a bit more challenging, since their API is very rate limited  
I opted to just download their latest data from 2020 and use that. Otherwise the data gathering would have taken a month+.  
After cleaning the data which also was a bit difficult since the API gave some hickups as well as the libraries.io data being
a bit scrambled I had useable raw datasets.
Those were cleaned and trimmed down to the most informative columns which I was then working with, and those were uploaded to AWS.

I've made heavy use of Bash scripts in this project to execute and feed additional parameters to the Python scripts that do the work.  
This was quite a bit new for me and I have to say that Bash is a great tool to have in the arsenal and I can just recommend everyone to learn it.  



#### What would happen if:
##### The data was increased by 100x? 
If the data was increased by this amount some parts of the ETL pipeline would have to be redone. The cleaning of the files  
already takes some time, that would need to be done faster by leveraging the power of Spark or some other method.
The AWS approach would still work although the cost would increase significantly, therefore some optimizations might be in order there too.  
I think with medium effort this project could be adapted to accommodate a 100x increase.

##### The ETL pipeline ran at 7am each day?  
The ETL pipeline is already almost ready to handle this scenario so this would not be an issue at all.   
All that was left to do was to have a scheduler that runs this and some small modifications so 'start.sh' doesn't require inputs.

##### The database needed to be accessed by 100 people?
Since we are using AWS Redshift as our Database this is also a nonissue. We could dynamically increase the EC2 machines  
if we are really struggling by hitting the DB with that many people although I do not think it would be necessary.  
I think this would at most need small modifications to the project in order to be done without issue.
<hr>

#### Why just two tables in Redshift?
I decided on this rather simple just two table structure in the Data Warehouse since this is a raw first insert of cleaned data,  
these tables would be used as an jumping off point for stakeholders that work with this data to create their own tables that contain the information necessary.
It is however already possible to join both tables together to get a "fuller" view of a Github repo.  

#### Why this ETL design?
The ETL is designed to work with the current infrastructure and be easily useable by anybody  
with just a little bit of tech knowledge. All that is needed is to clone the repo and execute two commands  
(and entering some configs).  
Staging the log and song files made sense because it made it much easier for us to insert the wanted data  
into the right tables, but also leaves us with the possibility of including more data or expanding our dimension or fact tables.

#### Why did you choose the cloud?
The cloud especially AWS was chosen just because of the dynamical scaling it provides.  
It's easy to just upload Millions of rows of data to it and rapidly prototype the Pipeline you have.
Also it's easy to scale up and down as needed and schedule the jobs etc.  
Another big plus is the 24/7 availability of the cloud and the reduction of on site overhead of personal.

#### Why did you choose Python?
Python was chosen because in the space of data, Python still has the best ecosystem to take care of all the needs of 
cleaning, gathering and distributing. All things I needed like Spark, AWS, Pandas and CSV readers were available for Python  
so this was a rather easy choice to make.


### ETL Workflow
 *Github* 
 1. Gather data from Github API (1,05Mil. Rows) Columns(ID, Name, full_name, owner_login, owner_id, owner_login(by mistake), owner_html_url, owner type, html_url, description, fork, language, forks_count, watchers_count, open_issues_count, is_template, topics, has_issues, has_projects, has_wiki, has_pages, has_downloads, created_at, updated_at, template_repo, archived, disabled).
 2. Clean the data gathered and drop unnecessary columns / rows. Columns that are kept: ID, Name, full_name, owner_login, owner_id,  owner type, html_url, description, fork 
 3. Dropped all rows that had "Null" in the owner or full_name columns. As well as all rows in ID that started with not a number (Planning).
 4. Dropped duplicate rows and saved the leftover data as gh_clean.csv

 *Libio*
 1. Downloaded the full dataset from the provided link (see uptop)
 2. Split the data into CSV's of 1Mil. rows each. Raw columns ('ID', 'Host Type', 'Name with Owner', 'Description', 'Fork',
       'Created Timestamp', 'Updated Timestamp', 'Last pushed Timestamp',
       'Homepage URL', 'Size', 'Stars Count', 'Language', 'Issues enabled',
       'Wiki enabled', 'Pages enabled', 'Forks Count', 'Mirror URL',
       'Open Issues Count', 'Default branch', 'Watchers Count', 'UUID',
       'Fork Source Name with Owner', 'License', 'Contributors Count',
       'Readme filename', 'Changelog filename',
       'Contributing guidelines filename', 'License filename',
       'Code of Conduct filename', 'Security Threat Model filename',
       'Security Audit filename', 'Status', 'Last Synced Timestamp',
       'SourceRank', 'Display Name', 'SCM type', 'Pull requests enabled',
       'Logo URL', 'Keywords') 
 3. Drop columns not needed so we end up with the final columns 
        'Host Type', 'Name with Owner', 'Description', 'Fork',
       'Created Timestamp', 'Updated Timestamp', 'Last pushed Timestamp',
       'Homepage URL', 'Stars Count', 'Language', 'Issues enabled',
       'Wiki enabled', 'Pages enabled', 'Forks Count', 'Mirror URL',
       'Default branch', 'Watchers Count', 'UUID',
       'Fork Source Name with Owner', 'Contributors Count', 'Readme filename',
       'Changelog filename', 'SourceRank', 'Display Name'
 4. Clean the data. Drop all rows where Homepage URL is over 70 characters.
    Drop all rows where Readme Filename is under 20 characters.
    Drop all rows where Readme Filename starts with just a t and has no other characters in the name.
    Drop all rows where the columns are shifted (e.g. in Timestamps have "false").
 5. Make a "sizedescription" column that converts the description column into a bitsize number.
    If this number is over 65534 then we drop the row.
    This is because the max length of text AWS Redshift can store is 65535Bits long.
    If we clean the data like this, this insert issue is entierly avoided.
6. Drop the "sizedescription" column and drop all duplicate rows. Save the csv as clean_xx.csv

Now to note is that the "Name with Owner" in the Libraries.io and the "Full_name" column in Github's data is overlapping.
This is the column on which you can join these two datasets in order to gain more information about a repo.

Beneath I will show a couple of example queries you can do in Redshift and the data you should get out.

1. Test if the Github table has data.   
    *Query* -> SELECT COUNT(DISTINCT(full_name)) FROM gh   
    *Answer* -> 998788 
    These are our unique rows after all cleaning that are now in the "gh" table.

2. See what the first 10 distinct results look like where the name starts with t.   
*Query* -> SELECT DISTINCT(full_name), description FROM gh WHERE full_name LIKE 't%' LIMIT 10; 
*Answer* ->   


| full_name | description |    
| -------- | ------- |    
| tesla42/test-repo | my First test repo |     
| toxicniggah/pytesto | - |     
| tramontane/mrrocpp | Multi-Robot Research Oriented Controller |     
| tsuwako/python-aelp | GAE startup files |   
| tsnoad/Address-Validation-using-QAS | scripts to interface between a database and QAS Pro API |     
| trisulnsm/trisul_ruby | Ruby helper for Trisul Remote Protocol |    
| testappid/code- test | - |  
| teeks99/py-largeupload | Python Large File Upload |   
| tekimaki/storage | - |  
| thiago-sanchez/beginning-perl | Projeto de tradução do livro Beginning Perl (Simon Cozens) |  

3. Let's see what the average stars_count is in the lib table.   
*Query* -> SELECT AVG(STARS_COUNT) FROM lib  
*Answer* -> 60.4859...

4. We can also see how many joined rows we get if we combine both tables.
*Query* -> SELECT COUNT(\*) FROM gh JOIN lib ON gh.full_name = lib.name_with_owner;  
*Answer* -> 87039  
So in total we have 87k rows that we have combined with just our sample data.
If we make a new table with the combined results we can now start to analyze the data together.

This data can be used in order to find more information on Github repos. Such as avg. stars, languages used or how many repos are updated regularly or recently.


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [AWS](https://aws.amazon.com/)
* [Spark](https://spark.apache.org/)
* Bash


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how can get the project working from your machine.
Be mindful that this will make a Redshift cluster with your AWS account.

I have included links to download the clean Github data already (I could not upload the raw data) as well as a clean libraries.io file so you can use the repo as is  
without having to gather data from the API or download the Libraries.io files.
If you want more data you can download the libraries.io files as well as increase the data gathering from the Github API.  
Note: If the links for the example data are expired please write me so I can renew them.
### Prerequisites
 * [Python](www.python.org)
 * [AWS-Acount](https://aws.amazon.com/)
 * Python virtualenv
 * [libraries.io data (V 1.6)](https://zenodo.org/record/3626071)[Optional]
 * [Github Clean example data](https://we.tl/t-rxuYSehqB8)
 * [Libraries.io Clean example data](https://we.tl/t-Jpwjz99GaV)
   ```sh
   pip install virtualenv 
   ```

### Installation
1. Clone the repo of the branch you want.
   ```sh
   git clone https://github.com/maximiliansoerenpollak/udacitycapstone
   ```

2. Open a terminal and navigate to the folder where you cloned the repo and make a virtual environment.
   ```sh
      cd place/you/cloned/repo/udacitycapstone
   ```
   Activate and install all requirements
   
   ```sh
      python3 -m venv name_of_virtualenv
      source name_of_virtualenv/bin/activate
      pip -r install requirements.txt
   ```
   Now you should have all requirements installed that are needed for the project.

3. If you downloaded the complete Libraries.Io file move the lib_repo.csv into the 'data/libcsv/' folder.
If you did not do that and instead used the Example Data then you need to move the gh_clean.csv into 'data/github/clean' and 
the clean_0.csv into '/data/libcsv/clean/'.


4. You first have to open up the dwh-empty.cfg and fill out all the input there.
   Make sure you create a new IAM  role in your AWS account since you do not want
   to enter your admin accounts information. 
   I explained underneath what to fill out where.

   ```
    [CLUSTER]
    DWH_CLUSTER_IDENTIFIER=Name_you_give_your_cluster
    DB_NAME=name_of_the_database
    DB_USER=name_of_the_iam_user
    DB_PASSWORD=
    DB_PORT=5439
    DWH_ROLE=Role_you_want_to_create_for_this_user

    [DWH] 
    DWH_CLUSTER_TYPE=multi-node
    DWH_NUM_NODES=4
    DWH_NODE_TYPE=dc2.large
    region=The_region_you_want_to_create_the_services_in

    [KEYS]
    ACCESS_KEY=Access_key_for_the_iam_user
    SECRET_KEY=secret_key_for_the_iam_user
   ```
    Once you have filled this out with the correct information, save it as `dwh.cfg`.
    All the other information that is not yet in this dwh.cfg will be filled out as the program runs. 

4.  After you have saved the config as `dwh.cfg`, filed it all in and moved the lib_repo.csv in the right folder you can start the process.
    All you have to do is to go into the folder where you cloned the project and run the start script.
    ```sh
    #Make the shellscript exectuable and start it 
    chmod +x start.sh
    ./start.sh
    ```
    This script will guide you through the whole process of cleaning the data and getting AWS up.
    Please Note: If you use the data provided by me, you can skip the Data Collection of the Github API as well as the cleaning, but you still need to  the LibIO data.  
    This should then startup the AWS cluster, create all needed Tables and move the data into them.
5. If you want to shut down all created AWS resources, just run `python aws_shutdown.py`.
   This will delete the Redshift cluster,S3 Bucket and the Role and Policies you created.



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Maximilain Soeren Pollak - pollakmaximilian@gmail.com

Project Link: [https://github.com/maximiliansoerenpollak/portfolio-api](https://github.com/maximiliansoerenpollak/udacitycapstone)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/maximiliansoerenpollak/udacitycapstone
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/msoerenpollak


