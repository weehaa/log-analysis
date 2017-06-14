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


def topArticles(limit=3):
    """ Returns sorted list of `limit` popular articles
    with the most popular article at the top."""

    db, cursor = connect()

    query = """SELECT a.title, count(l.path) views FROM articles a
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY a.title
               ORDER BY views DESC
               LIMIT (%s)"""
    params = (limit,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db.close()
    return rows
