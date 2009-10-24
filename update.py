#!/usr/bin/env python
"""
Scan twitter search results, remove irrelevant stuff, update database, render out main page
"""
import time
import simplejson
import pprint
import urllib2, urllib
import random
import re
import psycopg2

conn = psycopg2.connect("dbname='oneletteroffmovies' user='richard' host='localhost'")

class TwitterSearch(object):
    last_id = None
    term = None

    def __init__(self, term):
        self.term = term

    def fetch(self, limit, last_id):
        """
        Search
        """
        
        query = dict(q=self.term)
        if last_id:
            query['since_id'] = last_id
	try:
        	fh = urllib2.urlopen('http://search.twitter.com/search.json?%s' % urllib.urlencode(query))
	except Exception, e:
		time.sleep(60)
		return []
        result = simplejson.load(fh)
        
        
        return result['results']
        
def clean(s):
    s = s.replace('#oneletteroffmovies','')
    s = re.sub(r'[rR][tT] ','',s)
    s = re.sub(r' [rR][tT]','',s)
    s = re.sub(r'\([^\)]*\)','',s)
    s = re.sub(r'@[^ ]+','',s)
    s = re.sub(r'#[^ ]+','',s)
    s = re.sub(r'&[^;]+;','',s)
    s = re.sub(r'[ ]+',' ',s)
    return s.strip()

def normalize(s):
    s = clean(s)
    s = s.lower().strip()
    s = re.sub(r'[\-\.,]','',s)
    s = re.sub(r'[ ]+',' ',s)
    return s
        
ts = TwitterSearch('#oneletteroffmovies')

cur = conn.cursor()
cur.execute("SELECT MAX(id) FROM entries")
last_id = cur.fetchone()

for m in ts.fetch(500, last_id):
    cur.execute("""SELECT add_movie(%s, %s, %s, %s, %s, %s)""", [int(m['id']), m['from_user'], str(m['from_user_id']), m['profile_image_url'], clean(m['text']), normalize(m['text'])])
    print clean(m['text'])
    conn.commit()
    cur.execute("SELECT MAX(id) FROM entries")
    last_id = cur.fetchone()



