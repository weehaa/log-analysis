#!/usr/bin/env python
""" This module is a plain text reporting tool that prints reports
based on the data from the `news` database"""

import psycopg2


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection
    and a cursor."""
    try:
        print('Trying to connect to `{}` database...'.format(database_name))
        db_conn = psycopg2.connect("dbname={}".format(database_name))
    except psycopg2.OperationalError as db_exept:
        print('Unable to connect!\n{0}').format(db_exept)
        quit()
    else:
        print('Connected!')
        cursor = db_conn.cursor()
        return db_conn, cursor


def top_articles(limit=3):
    """ Prints sorted list of `limit` popular articles
    with the most popular article at the top."""

    db_conn, cursor = connect()

    query = """SELECT a.title, count(l.path) views FROM articles a
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY a.title
               ORDER BY views DESC
               LIMIT (%s)"""
    params = (limit,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db_conn.close()
    print("\nThe most popular {} articles of all time:\n".format(limit))
    i = 1
    for row in rows:
        print(str(i) + ". \"{title}\" - {viewsCount} views".
              format(title=row[0], viewsCount=row[1]))
        i += 1
    print
    return


def top_authors(limit=3):
    """ Prints sorted list of `limit` authors, that get
    the most page views with the most popular author at the top."""

    db_conn, cursor = connect()

    query = """SELECT au.name, count(a.id) views FROM authors au
               LEFT JOIN articles a ON au.id = a.author
               GROUP BY au.name
               ORDER BY views DESC
               LIMIT (%s)"""
    params = (limit,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db_conn.close()
    print("\nThe most popular {} authors of all time:\n".format(limit))
    i = 1
    for row in rows:
        print(str(i) + ". {author} - {viewsCount} views".
              format(author=row[0], viewsCount=row[1]))
        i += 1
    print
    return


def errors_by_day(threshold=1):
    """ Prints sorted list of days, which percentage of http errors
    was more than the threshold (1% by default)."""

    db_conn, cursor = connect()

    query = """SELECT to_char(l.time, 'FMMONTH DD, YYYY') date_time,
                        100.0 * SUM(CASE
                                    WHEN l.status <> '200 OK' THEN 1
                                    ELSE 0
                               END)
                               /
                               (CASE count(l.status)
                                    WHEN 0 THEN 1
                                    ELSE count(l.status)
                                END) err_pcnt
            FROM log l
            GROUP BY date_time HAVING 100.0 * SUM(CASE
                        WHEN l.status <> '200 OK' THEN 1
                        ELSE 0
                   END)
                   /
                   (CASE count(l.status)
                        WHEN 0 THEN 1
                        ELSE count(l.status)
                    END) > (%s)
            ORDER BY err_pcnt DESC"""

    params = (threshold,)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    db_conn.close()

    print("\nDays when more than {}% of requests lead to errors:\n".
          format(threshold))
    for row in rows:
        print("{day} - {errPcnt}% errors".
              format(day=row[0], errPcnt=round(row[1], 1)))
    print
    return

top_articles()
top_authors()
errors_by_day()
