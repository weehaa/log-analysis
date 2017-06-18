#!/usr/bin/env python
""" This module is a plain text reporting tool that prints reports
based on the data from the `news` database"""

import psycopg2
from functools import wraps


def is_pos_integer(func):
    '''Check that argument is a non-negative integer'''
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


def get_query_results(query, params=None):
    """ Connects to a database, executes query and returns a result """
    # connect to database and grab cursor
    db_conn, cursor = connect()
    # execute
    cursor.execute(query, params)
    result = cursor.fetchall()
    # close connection
    db_conn.close()
    # return results
    return result


@is_pos_integer
def top_articles(limit):
    """ Prints sorted list of `limit` popular articles
    and their number of views with the most popular article at the top.
    If limit is set to 0, prints all the articles"""

    query = """SELECT a.title, count(l.path) FROM articles a
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY a.title
               ORDER BY count(l.path) DESC"""

    rows = get_query_results(query)

    print("\nThe most popular {} articles of all time:\n".
          format(limit if limit else "all"))

    # if limit = 0 then return all rows
    row_cnt = limit if limit else len(rows)

    for i in range(row_cnt):
        print(str(i+1) + ". \"{title}\" - {viewsCount} views".
              format(title=rows[i][0], viewsCount=rows[i][1]))
    print
    return


@is_pos_integer
def top_authors(limit):
    """ Prints sorted list of `limit` authors, that get
    the most page views with the most popular author at the top.
    If `limit` is set to 0, prints all the authors"""

    query = """SELECT au.name, count(l.path) FROM authors au
               LEFT JOIN articles a ON au.id = a.author
               LEFT JOIN log l ON l.path = '/article/'||a.slug
               GROUP BY au.name
               ORDER BY count(a.id) DESC"""
    rows = get_query_results(query, params=None)

    print("\nThe most popular {} authors of all time:\n".
          format(limit if limit else ""))

    # if limit = 0 then return all rows
    row_cnt = limit if limit else cursor.rowcount

    for i in range(1, row_cnt+1):
        row = cursor.next()
        print(str(i) + ". {author} - {viewsCount} views".
              format(author=row[0], viewsCount=row[1]))
    print
    db_conn.close()
    return


@is_pos_integer
def errors_by_day(threshold):
    """ Prints sorted list of days, which percentage of http errors
    was more than the threshold."""

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
