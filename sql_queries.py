# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS times;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
  "id" SERIAL PRIMARY KEY,
  "start_time" TIMESTAMP REFERENCES times(start_time),
  "user_id" INT REFERENCES users(id) NOT NULL,
  "level" VARCHAR NOT NULL,
  "song_id" VARCHAR REFERENCES songs(id),
  "artist_id" VARCHAR REFERENCES artists(id),
  "session_id" INT NOT NULL,
  "location" VARCHAR NOT NULL,
  "user_agent" VARCHAR NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
  "id" INT UNIQUE NOT NULL,
  "first_name" VARCHAR,
  "last_name" VARCHAR,
  "gender" CHAR(1),
  "level" VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
  "id" VARCHAR UNIQUE NOT NULL,
  "title" VARCHAR,
  "artist_id" VARCHAR,
  "year" INT,
  "duration" NUMERIC
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
  "id" VARCHAR UNIQUE NOT NULL,
  "name" VARCHAR,
  "location" VARCHAR,
  "latitude" NUMERIC,
  "longitude" NUMERIC
);
""")

time_table_create = ("""
CREATE TABLE times (
  "start_time" TIMESTAMP UNIQUE NOT NULL,
  "hour" INT,
  "day" INT,
  "week" INT,
  "month" INT,
  "year" INT,
  "weekday" VARCHAR
);
""")

# INSERT RECORDS

user_table_insert = ("""
INSERT INTO users (id, first_name, last_name, 
                   gender, level)
VALUES (%s, %s, %s, 
        %s, %s)
ON CONFLICT (id)
DO UPDATE 
SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (id, title, artist_id, 
                   year, duration)
VALUES (%s, %s, %s, 
        %s, %s)
ON CONFLICT (id)
DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (id, name, location, 
                     latitude, longitude)
VALUES (%s, %s, %s, 
        %s, %s)
ON CONFLICT (id)
DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO times (start_time , hour, day, 
                   week, month, year, weekday)
VALUES (%s, %s, %s, 
        %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING;
""")

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, 
                        song_id, artist_id, session_id, 
                        location, user_agent)
VALUES (%s, %s, %s,
        %s, %s, %s,
        %s, %s);
""")

# FIND SONGS

song_select = ("""
SELECT
    s.id song_id,
    a.id artist_id
FROM songs s
LEFT JOIN artists a
    ON s.artist_id = a.id
WHERE s.title = (%s)
AND a.name = (%s)
AND s.duration = (%s);
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, 
                        artist_table_create, time_table_create, 
                        songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, 
                      song_table_drop, artist_table_drop, 
                      time_table_drop]