# Using song_dataset to query songs details. Will discard duplicate values hence using distinct.
songs_table_query = "SELECT distinct song_id, title as song_title, artist_id, year, duration FROM songs"

# Using song_dataset to query artist details. Will discard duplicate values hence using distinct.
artists_table_query = "SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude FROM songs"

# Using log_dataset to query log_event details where page = NextSong
log_filtered_query = "SELECT *, cast(ts/1000 as Timestamp) as timestamp from log_events where page = 'NextSong'"

# Using filtered log_dataset to query user details
users_query = "SELECT userId, firstName, lastName, gender, level from log_events"

# Time table query from log_events view
time_query = ("""
    select distinct timestamp as start_time, 
    hour(timestamp) as hour, 
    day(timestamp) as day, 
    weekofyear(timestamp) as week, 
    month(timestamp) as month, 
    year(timestamp) as year, 
    weekday(timestamp) as weekday
    from log_events """)

# Simple inner join based on the song_title.
songplays_query = ("""
    select a.timestamp as start_time, a.userId, a.level, b.song_id, b.artist_id, a.sessionId, a.location, a.userAgent, year(a.timestamp) as year, month(a.timestamp) as month 
    from log_events as a 
    inner join songs as b on a.song = b.song_title """)