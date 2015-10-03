#!/usr/bin/env python

import requests
import json
import csv
from bs4 import BeautifulSoup

sections = [
    (187413, 'Open_u18'),
    (187414, 'Open_u16'),
    (187415, 'Open_u14'),
    (187416, 'Open_u12'),
    (187417, 'Open_u10'),
    (187418, 'Open_u08'),
    (187419, 'Girls_u18'),
    (187420, 'Girls_u16'),
    (187421, 'Girls_u14'),
    (187422, 'Girls_u12'),
    (187423, 'Girls_u10'),
    (187424, 'Girls_u08'),
]

url = 'http://chess-results.com/tnr%s.aspx?lan=1&art=0&turdet=YES&flag=30&wi=984&zeilen=99999'

for section in sections:
    print 'Fetching section:', section[1]
    r = requests.get(url % section[0])
    if r.status_code == 200:
        with open(os.path.join('lists', '%s.csv' % section[1]), 'w') as f:
            writer = csv.writer(f)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.findAll('table', {'class': 'CRs1'})[0]
            for row in table.findAll('tr')[1:]:
                writer.writerow([td.text for td in row])
