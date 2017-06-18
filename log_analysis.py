#!/usr/bin/env python
""" This module is a plain text reporting tool that prints reports
based on the data from the `news` database"""

import psycopg2
from functools import wraps


def is_pos_integer(func):
    '''Check that argument is an non-negative integer'''
    @wraps(func)
    def decorated_function(arg):
        try:
            int(' ') if arg < 0 else int(arg)
        except ValueError:
            print ("ERROR: \"" + str(arg) + "\" is not a valid argument for " +
                    func.__name__ + " function, please type 0,1,2,3...")
            return
        else:
            return func(arg)
    return decorated_function


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection
    and a cursor."""
    try:
        # print('Trying to connect to `{}` database...'.format(database_name))
        db_conn = psycopg2.connect("dbname={}".format(database_name))
    except psycopg2.OperationalError as db_except:
        print('Unable to connect!\n{0}').format(db_except)
        quit()
    else:
        # print('Connected!')
        cursor = db_conn.cursor()
        return db_conn, cursor


@is_pos_integer
def top_articles(limit):
    """ Prints sorted list of `limit` popular articles
    with the most popular article at the top."""

    db_conn, cursor = connect()

    query = """SELECT a.title, count(l.path) FROM articles a
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY a.title
               ORDER BY count(l.path) DESC"""
    cursor.execute(query)

    print("\nThe most popular {} articles of all time:\n".
            format(limit if limit else "all"))

    # if limit = 0 then return all rows
    row_cnt = limit if limit else cursor.rowcount

    for i in range(1, row_cnt+1):
        row = cursor.next()
        print(str(i) + ". \"{title}\" - {viewsCount} views".
              format(title=row[0], viewsCount=row[1]))
    print
    db_conn.close()
    return


def top_authors():
    """ Prints sorted list of `limit` authors, that get
    the most page views with the most popular author at the top."""

    db_conn, cursor = connect()

    query = """SELECT au.name, count(l.path) FROM authors au
               LEFT JOIN articles a ON au.id = a.author
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY au.name
               ORDER BY count(a.id) DESC"""
    cursor.execute(query)
    rows = cursor.fetchall()

    db_conn.close()
    print("\nThe most popular authors of all time:\n")
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

    query = """SELECT to_char(date, 'FMMONTH DD, YYYY') AS "date",
                err_pcnt from
                (SELECT date_trunc('day', l.time) AS "date",
                            100.0 * SUM(CASE
                                        WHEN l.status <> '200 OK' THEN 1
                                        ELSE 0
                                   END)
                                   /
                                   (CASE count(l.status)
                                        WHEN 0 THEN 1
                                        ELSE count(l.status)
                                    END) AS "err_pcnt"
                FROM log l
                GROUP BY date HAVING 100.0 * SUM(CASE
                            WHEN l.status <> '200 OK' THEN 1
                            ELSE 0
                       END)
                       /
                       (CASE count(l.status)
                            WHEN 0 THEN 1
                            ELSE count(l.status)
                        END) > (%s)
                ORDER BY err_pcnt DESC) AS "err_info"
                """

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
