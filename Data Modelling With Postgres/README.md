Udacity - Data Engineering Nanodegree
-------------------------------------

Project: Data Modeling with Postgres
------------------------------------

Summary
-------
The startup Sparkify has a music streaming app, and its data related to songs, artists and listening behavior resides in JSON files. There are two main types of files:

1. JSON logs on user activity on the app
2. JSON metadata on the songs available in the app

Currently, the analytics team of the company is interested in analyzing what songs users of the app are listening to. Therefore, the purpose of this project is to create a database designed to optimize queries on song play analysis, and import the data stored in the JSON files into that database.

Creating the database
---------------------

The creation of the database tables and ETL processes for each table were developed in Python scripts.

The script create_tables.py creates the database sparkifydb and the five tables of the star schema described in the previous section. The CREATE and DROP statements called by that script are defined in another script, sql_queries.py.

To proceed with the creation of the tables, run the following command in the terminal:

python create_tables.py
This command can be rerun as much as needed in order to reset the tables, since the script create_tables.py also contains statements to drop both the tables and the sparkifydb database if they exist.

Importing the data
-------------------

Once the tables have been properly created, the database will be ready to be populated with the data stored in the JSON files.

The ETL processes are defined in the file etl.py. This script contains a number of Python functions that, together, process all the song and log files in the directories data/song_data and data/log_data and loads the data in the dimension and fact tables of the sparkifydb database.

In order to import the JSON files data into the database, run the following command in the terminal: python etl.py

The output of that script shows how many files were processed. Run test.ipynb to confirm the records were successfully inserted into each table.