#!/usr/bin/env python
""" This module just runs all reports from log_analysis module"""

import log_analysis as l

l.top_articles(3)
l.top_authors(0)
l.errors_by_day(1)
