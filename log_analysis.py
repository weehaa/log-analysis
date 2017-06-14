#!/usr/bin/env python
#
# log_analysis.py -- reporting tool that prints reports in plain text
# based on the data in the `news` database
#

import psycopg2


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection
    and a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("ERROR: Can't connect to {} database".format(database_name))
        quit()

        
