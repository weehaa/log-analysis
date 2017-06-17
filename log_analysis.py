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
    print("\nThe most popular {} articles of all time:\n".format(limit))
    i = 1
    for row in rows:
        print(str(i) + ". \"{title}\" - {viewsCount} views".\
             format(title = row[0], viewsCount = row[1]))
        i+=1
    print("\n")
        print(str(i) + ". \"{title}\" - {viewsCount} views".
              format(title=row[0], viewsCount=row[1]))
        i += 1
    print
    return


def topAuthors(limit=3):
    """ Returns sorted list of `limit` authors, that get
    the most page views with the most popular author at the top."""

    db, cursor = connect()

    query = """SELECT au.name, count(a.id) views FROM authors au
               LEFT JOIN articles a ON au.id = a.author
               GROUP BY au.name
               ORDER BY views DESC
               LIMIT (%s)"""
    params = (limit,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db.close()
    return rows
    print("\nThe most popular {} authors of all time:\n".format(limit))
    i = 1
    for row in rows:
        print(str(i) + ". {author} - {viewsCount} views".
              format(author=row[0], viewsCount=row[1]))
        i += 1
    print
    return

def topErrorsByDay(limit=3):
    """ Returns sorted list of `limit` days, with http errors percentage."""

    db, cursor = connect()

    query = """SELECT  100.0 * SUM(CASE
                                    WHEN l.status <> '200 OK' THEN 1
                                    ELSE 0
                               END)
                               /
                               (CASE count(l.status)
                                    WHEN 0 THEN 1
                                    ELSE count(l.status)
                                END) err_pcnt,
                    to_char(l.time, 'FMMONTH DD, YYYY') date_time
            FROM log l
            GROUP BY date_time
            ORDER BY err_pcnt DESC
            LIMIT (%s)"""
    params = (limit,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db.close()
    return rows
