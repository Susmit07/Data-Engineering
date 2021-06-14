import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from sql_queries import songs_table_query, artists_table_query, log_filtered_query, users_query, time_query, songplays_query

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    """
    This function reads the songs JSON files from S3 and processes them with Spark.
    We separate the files into specific dataframes the represent the tables.
    Then, these tables are saved back to the output folder indicated by output_data parameter.
    
    Arguments:
        spark: Spark session = The entry point to programming Spark with the Dataset and DataFrame APIs.
        input_data (:obj:`str`): Directory to find the JSON input files in S3.
        output_data (:obj:`str`): Directory  to save parquet files in S3.
    """
    
    # get filepath to song data file
    # song_data/A/A/B/TRAABJL12903CDCF1A.json (matching with wild-characters.)
    song_data = input_data + "song_data/*/*/*/*.json"
    
    # read song data file
    df = spark.read.json(song_data)
    # Temporary view will be used in all our related queries. Will no persist it in-memory.
    df.createOrReplaceTempView("songs")

    # extract columns to create songs table
    songs_table = spark.sql(songs_table_query)
    
    # write songs table to parquet files partitioned by year and artist_id, it will be overwritten everytime the script is executed. 
    songs_table.write.partitionBy("year", "artist_id").parquet(path = output_data + "/songs/songs.parquet", mode = "overwrite")

    # extract columns to create artists table
    artists_table = spark.sql(artists_table_query)
    
    # write artists table to parquet files
    artists_table.write.parquet(path = output_data + "/artists/artists.parquet", mode = "overwrite")


def process_log_data(spark, input_data, output_data):
    """
    This function reads the logs JSON files from S3 and processes them with Spark.
    We separate the files into specific dataframes the represent the tables.
    Then, these tables are saved back to the output folder indicated by output_data parameter.
    
    Arguments:
        spark: Spark session = The entry point to programming Spark with the Dataset and DataFrame APIs.
        input_data (:obj:`str`): Directory to find the JSON input files in S3.
        output_data (:obj:`str`): Directory  to save parquet files in S3.
    """
    
    # get filepath to log data file
    # log_data/2018/11/2018-11-13-events.json (matching with wild-characters.)
    log_data = input_data + "log_data/*/*/*.json"

    # read log data file
    df = spark.read.json(log_data)
    # Temporary view will be used in all our related queries. Will no persist it in-memory.
    df.createOrReplaceTempView("log_events")
    
    # filter by actions for song plays
    df = spark.sql(log_filtered_query)
    
    # Replacing the previously created temp view with the filtered data.
    df.createOrReplaceTempView("log_events")

    # extract columns for users table    
    users_table = spark.sql(users_query).dropDuplicates(['userId'])
    
    # write users table to parquet files
    users_table.write.parquet(path = output_data + "/users/users.parquet", mode = "overwrite")
    
    # extract columns to create time table
    time_table = spark.sql(time_query)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(path = output_data + "/time/time.parquet", mode = "overwrite")

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + "/songs/songs.parquet")
    # create a temp view, will use it as a join table while creating the final songplays table
    song_df.createOrReplaceTempView("songs")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql(songplays_query)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(path = output_data + "/songplays/songplays.parquet", mode = "overwrite")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    # A bucket named udacity-sparkify where all parquet files will be stored.
    output_data = "s3a://udacity-sparkify/data-lake-out/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()