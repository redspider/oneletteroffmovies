#!/usr/bin/env python
"""
Retrieve most popular, render out
"""
import time
import simplejson
import pprint
import urllib2, urllib
import random
import re
import psycopg2, psycopg2.extras
from mako.template import Template

conn = psycopg2.connect("dbname='oneletteroffmovies'")
conn.set_client_encoding('utf8')


cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("SELECT qname, author_name, author_id, profile_image, movie, count FROM movies JOIN entries ON movies.best = entries.id WHERE count > 1 AND movie != '' ORDER BY movies.count DESC LIMIT 30")
results = cur.fetchall()

template = Template(open("index.html","r").read())
out_handle = open('output/index.html','w')
out_handle.write(template.render(results=results))
out_handle.close()



