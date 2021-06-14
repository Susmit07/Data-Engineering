Data Engineering Capstone Project
---------------------------------

Project Summary
---------------

The project will involve exploring and assessment of data from different data-sets, and write to file storages for later processing based on business demands

Scope
-----

The project will address - cleansing, processing of data from multiple data sources (mainly file-systems) and finally storing the cleansed data in file-storage (csv, parquet, json etc.). Finally we will perform minimilastic code quality checks on the dataframes.

Data Sets used:
---------------

The Data Sets used to complete this project:

1. I94 Immigration Data : Comes from the U.S. National Tourism and Trade Office and contains various statistics on international visitor arrival in USA and comes from the US National Tourism and Trade Office.
2. World Temperature Data: Comes from Kaggle and contains average weather temperatures by city.
3. U.S. City Demographic Data: Comes from OpenSoft and contains information about the demographics of all US cities such as average age, male and female population
4. Airport codes and related cities : Comes from https://datahub.io/core/airport-codes#data. Airport codes data contains information about different airports around the world.
5. Climate Change: Earth Surface Temperature Data : Comes from Kaggle. Contains temperature for earth surface temperature data.

Data Model:
----------
The data model consists of tables immigration, DEMOGRAPHICS, AirportCodes, GlobalLandTemperature, i94cit_res, i94port, i94mode, i94address, i94visa. Please refer to the Data Model.png file in project root location for detailed diagrammatic representation.

Data Dictionary:
----------------
Please refer to the Data Dictionary.png file in project root location for detailed diagrammatic representation.


Choice of tools and technologies for the project
------------------------------------------------

Pandas and Spark libraries are used to ease data preprocessing. Both the libraries are helpful to efficiently load and manipulate data. At a later stage, instead of pandas dataframes, I recommend using Spark dataframes to allow distributed processing using for example Amazon Elastic Map Reduce (EMR) (currently in not actual scope of the project). Also, to perform automated updates, I recommend integrating the ETL pipeline into an Airflow DAG. (currently not in the actual project implementation, but can be integrated with)

I used a Jupyter Notebook to show the data structure and the need for data cleaning. I used Python 3 as a programming language. For the data model diagram I used SQLDBM

Data Exploration & Modeling of different data sets explained:
------------------------------------------------------------

1. Data Exploration & Modeling for U.S. City Demographic Data
   
Steps Involved:
---------------

i.   Data Read from CSV file
ii.  Process the data (convert all columns from string to integer and double type) and perform aggregation
iii. Modify the column name and fill all null values with 0
iv.  Finally, write to a parquet folder

2. Data Exploration & Modeling for I94 Immigration Data 

Steps Involved:
--------------

i.    Data Read from sas_data folder (comprising of I94 Immigration parquet data in chunks)
ii.   Process the data (convert necessary columns from string to integer, double type and date type), needed downstream for date calculation  
iii.  Remove unwanted columns.
iv.   Finally, write to a parquet folder immigration

3. Data Exploration & Modeling for I94 Immigration Data (I94_SAS_Labels_Descriptions.SAS file)

Steps Involved:
---------------

i.   Data Read from I94_SAS_Labels_Descriptions file
ii.  Process the data and prepare the data (below cell)
iii. Parse based on the country, port, mode, address and visa-type

4. Data Exploration & Modeling for I94 Immigration Data

Steps Involved:
--------------

i.   Data Read from sas_data folder (comprising of I94 Immigration parquet data in chunks)
ii.  Process the data only select necessary columns needed for calculation
iii. Remove duplicates.
iv.  Extract month, year, day of month, week, day of year and store in a temporary view
v.   Query the view and create a new column "Quarter", populate the column based on the month condition
vi.  Finally write to a parquet file, with partition arrival_year and arrival_month

5. Data Exploration & Modeling for Global Temperature by City (GlobalLandTemperaturesByCity.csv file)

Steps Involved:
--------------

i.  Data Read from GlobalLandTemperaturesByCity file
ii.  Process the data and only keep data related to United States
iii. Store in a CSV file finally GlobalLandTempOfUS.csv

6. Data Exploration & Modeling for Aiport Codes

Steps Involved:
--------------

i.   Data Read from Aiport codes csv file
ii.  Process the data split the coordinates column to 2 sperate columns, latitude and longitude
iii. Store in a CSV file finally filtered_location_data.csv with necessary filtered columns

Data Quality Checks for all pre-processed data.
-----------------------------------------------

Steps Involved:
---------------
i.   Create a spark temp view based on the individual data frame object
ii.  Query the view to check if proper count is returned.
iii. Query the view to check if any null value is being present in any calculated column.

Execution Steps:
----------------

i. The project should be executed from the python notebook file : Capstone Project Template.ipynb
ii. The project is designed in a simple way and is primarily focussed heavily on processing the datas using Pandas and Spark api
iii. No external data source is used (like s3 or Redshift), but necessary hooks can be used to interact with the foreign storage client apis to persist the processed data.
iv. Apache Airflow is not integrated with the project for taskflow scheduling, but can be integrated

FAQs: What would a data engineer do if...
-------------------------------------------

During heavy peak work loads we can find multiple issues, when the application is tested to the maximum limit. I will be addressing the issue with respect to the Capstone project with Cassandra as a database.

1. The data is increased by 100x & heavy write operations

Use Spark framework to process the data efficiently in a distributed enviroment e.g. with AWS EMR. In case the data engineer recognizes that there is a write-heavy operation going, I would suggest using a Cassandra database as writes are very fast in Cassandra due to the log-structured design, and written data is persisted with a Commit Log and then relayed to Memtable and SSTables(Sorted String Tables). Alongside if data is properly modeled, especially if data is distributed evenly among the partition keys cassandra will scale horizontally well.

2. The application encounters heavy read operations

Although cassandra is suitable for high write throughput rather than heavy reads, but we can design our data model as  mentioned in the below said points to achieve the heavy read operations:

i. Try to determine exactly what queries we need to support. During write itself we can group by an attribute, order by an attribute, filter data based on some condition and store in the corresponding table.
ii. Choose the Proper Row Key (partition key). The Partition Key is useful for locating the data in the node in a cluster, and the clustering key specifies the sorted order of the data within the selected partition. Selecting a proper partition key helps avoid overloading of any one node in a Cassandra cluster, and also improves the read throughput.
iii. Data duplication can be encouraged to achieve read efficiency, for instance a materialized views in order to cater a specific use case.
iv. If the query response pay load size is over 20 MB, consider additional cache or change in query pattern, as cassandra is not great at handling large size data.
v. Use materialized views with automatic updates to make reads faster.
vi. An index can be used as it provides a means to access data in Cassandra using a non-partition key. 

3. The data populates a dashboard that must be updated on a daily basis by 7am every day.

Use Airflow and create a DAG that performs the logic of the described pipeline. If executing the DAG fails, the dags should be configures to send emails automatically to the engineering team using Airflow's built-in feature ( email_on_failure=True), so they can fix potential issues soon.

3. The database needed to be accessed by 100+ people.

Cassandra is highly scalable all the nodes in the cluster will be sufficent enough to cater the 100+ simultaneous incoming requests, and forward to necessary partition via consistency hashing.

For consistency we can use QUORUM consistency, so client will wait for acknowledgement from (n/2+1) number of nodes in the cluster across different data centre, once the data is replicated. AWS Redshift can also be used for this specific use case, but client has to bear the billing.