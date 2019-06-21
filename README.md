# Data Modeling with PostgreSQL

## Background

A fake music streaming company, Sparkify, wants a database organized around the questions about what music users are listening to. The data currently resides in 2 JSON files, one logging activity and the other containing song metadata.

## Goals

1. Create a relational database with PostgreSQL using a star schema.
2. Populate the schema with a Python and SQL ETL pipeline from JSON files.
3. Perform lightly edited stream-of-consciousness EDA.

## To Do

- [x] Complete logical modeling with [dbdiagrams.io](https://dbdiagram.io).
- [x] Evaluate choice of data types
- [x] Remove PK constraint on artist_id? Two artist names with shared artist ids.
- [x] Complete process_log_file function

## Files

- `test.ipynb` displays the first few rows of each table to let you check the database.
- `create_tables.py` drops and creates tables. Run this file to reset the tables before running the ETL scripts.
- `etl.ipynb` reads and processes a single file from song_data and log_data and loads the data into tables. It was used to build the pipeline for `etl.py`
- `etl.py` reads and processes files from song_data and log_data and loads them into tables.
- `sql_queries.py` contains all sql queries, and is imported into the last three files above.
- `README.md` this file, provides discussion on project.
- `eda.ipynb` performs a basic analysis

## Database

The data is organized as a star schema, where the fact table is `songplays`, holding information directly related to a particular song play event. The connected dimension tables (`times`, `songs`, `users` and `artists`) provide access to more details related to song play events.

## Improvements

- Use TDD practices
- Use COPY instead of INSERT
- Create a table to keep track of user level changes
- Refactor time_data as comprehension

## Questions

- Where do you see opportunities for optimizing SQL and Python?
- What weaknesses do you see in the data model and the pipeline?

### Tools

- Anaconda for Python and Jupyter Lab
- Libraries
  - psycopg2
  - os
  - glob
  - pandas
  - numpy

### Issues Encountered

1. Error creating `time` table because the list of create table queries was out of order.
2. Error inserting data because query is empty.
3. Two artists have the same artist id. Chose to add ON CONFLICT DO NOTHING to INSERT statements.

### Resources

- Found [this explainer](https://towardsdatascience.com/jupyter-magics-with-sql-921370099589) on magic SQL in Jupyter Notebooks useful