#!/usr/bin/env python

import feedparser 


d = feedparser.parse("http://192.243.108.252/w/api.php?hidebots=1&urlversion=1&days=7&limit=50&action=feedrecentchanges&feedformat=atom")

for entry in d['entries']:
    print()
    for key in entry:
        print(key)
    print(entry['title'])
    print(entry['updated'])
