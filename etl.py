import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from numpy import datetime_as_string


def process_song_file(cur, filepath):
    """    
    Create tables for songs and artists from a JSON file.
    
    cur: (psycopg2.cursor) Database cursor
    filepath: (str) File location
    
    Preconditions
        Imports: psycopg2, sql_queries, pandas as pd
        Connections: Sparkify database
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_df = df.loc[:, ['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = tuple(song_df.values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_df = df.loc[:, ['artist_id', 'artist_name', 
                          'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = tuple(artist_df.values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """    
    Create tables for times, users and songplays from a JSON file.
    
    cur: (psycopg2.cursor) Database cursor
    filepath: (str) File location
    
    Preconditions
        Imports: psycopg2, sql_queries, pandas as pd, 
             from numpy import datetime_as_string
        Connections: Sparkify database
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    next_song_filter = df['page'] == 'NextSong'
    df = df[next_song_filter]

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit = 'ms')
    
    # insert time data records
    time_data = [list(datetime_as_string(df['ts'].values)), 
                 list(df['ts'].dt.hour.values), 
                 list(df['ts'].dt.day.values), 
                 list(df['ts'].dt.week.values), 
                 list(df['ts'].dt.month.values), 
                 list(df['ts'].dt.year.values), 
                 list(df['ts'].dt.weekday.values)]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.drop_duplicates(subset='userId')

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit = 'ms'), row.userId, row.level,
                     songid, artistid, row.sessionId,
                     row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """    
    Get all files in filepath, apply the function to the files 
    and print processing status.
    
    cur: (psycopg2.cursor) Database cursor
    conn: (psycopg2.connection) Database connection
    filepath: (str) File location
    func: (function) process_song_file or process_log_file
    
    Preconditions
        Imports: glob, os, psycopg2
        Connections: Sparkify database
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Establish a connection to the Sparkify database and execute ETL processes.
    
    Preconditions
        Imports: psycopg2
    
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data/2018/11', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()