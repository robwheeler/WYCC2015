#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import csv
import requests
import glob

url = 'http://chess-db.com/public/download.jsp?id='

# chess-db.com limits the number of games you can download if you aren't
# logged in.  Therefore, you need to register a user and log in, then
# extract the cookies from your web browser and add them here.

cookies = {
    # Insert JSESSIONID cookie here
    # 'JSESSIONID': '???'
}

if 'JSESSIONID' not in cookies:
    print('You must set the JSESSIONID cookie before using this script.', file=sys.stderr)
    sys.exit(-1)

for filename in glob.glob(os.path.join('lists', '*.csv')):
    print(filename)
    section = os.path.splitext(os.path.basename(filename))[0]
    with open(os.path.join('PGNs', '{}.pgn'.format(section)), 'w') as outfile:
        with open(filename) as infile:
            reader = csv.reader(infile)
            for row in reader:
                r = requests.get(url + row[4], cookies=cookies)
                if r.status_code == 200:
                    outfile.write(r.content)
                else:
                    print('Could not find games for {}: {}'.format(row[3], r.status_code), file=sys.stderr)

sys.exit(0)
