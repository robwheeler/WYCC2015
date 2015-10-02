#!/usr/bin/env python

url = 'http://chess-db.com/public/download.jsp?id='

import os
import sys
import csv
import requests
import glob

# chess-db.com limits the number of games you can download if you aren't
# logged in.  Therefore, you need to register a user and log in, then
# extract the cookies from your web browser and add them here.
cookies = {
    #'JSESSIONID': '???',
    #'_gat': '1',
    #'__utmt': '1',
    #'__utma': '???',
    #'__utmb': '???',
    #'__utmc': '???',
    #'__utmz': '???',
    #'_ga': '???',
}

for filename in glob.glob('lists/*.csv'):
    print filename
    section = filename.split('/')[1].split('.')[0].replace(' ', '_')
    with open('PGNs/%s.pgn' % section, 'w') as outfile:
        with open(filename) as infile:
            reader = csv.reader(infile)
            for row in reader:
                r = requests.get(url + row[4], cookies=cookies)
                if r.status_code == 200:
                    outfile.write(r.content)
                else:
                    print 'Could not find games for %s: %s' % (row[3], r.status_code)

sys.exit(0)
