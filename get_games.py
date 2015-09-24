#!/usr/bin/env python

url = 'http://chess-db.com/public/download.jsp?id='

import os
import sys
import csv
import requests

#JSESSIONID=FBF984C7A72EC3B9E4853CA0298C9BBA
cookies = {
    'JSESSIONID': 'FBF984C7A72EC3B9E4853CA0298C9BBA',
    '_gat': '1',
    '__utmt': '1',
    '__utma': '250825556.1493689967.1442537242.1442537242.1442537242.1',
    '__utmb': '250825556.4.10.1442537242',
    '__utmc': '250825556',
    '__utmz': '250825556.1442537242.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '_ga': 'GA1.2.1493689967.1442537242',
}

for filename in os.listdir('lists/'):
    print filename
    with open('PGNs/%s.pgn' % filename.split('.')[0].replace(' ', '_'), 'w') as outfile:
        with open(os.path.join('lists', filename)) as infile:
            reader = csv.reader(infile)
            for row in reader:
                r = requests.get(url + row[4], cookies=cookies)
                if r.status_code == 200:
                    outfile.write(r.content)
                else:
                    print 'Could not find games for %s: %s' % (row[3], r.status_code)

sys.exit(0)
