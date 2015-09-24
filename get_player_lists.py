#!/usr/bin/env python

import requests
import json
import csv
from bs4 import BeautifulSoup

sections = [
    (187413, 'Open u18'),
    (187414, 'Open u16'),
    (187415, 'Open u14'),
    (187416, 'Open u12'),
    (187417, 'Open u10'),
    (187418, 'Open u08'),
    (187419, 'Girls u18'),
    (187420, 'Girls u16'),
    (187421, 'Girls u14'),
    (187422, 'Girls u12'),
    (187423, 'Girls u10'),
    (187424, 'Girls u08'),
]

url = 'http://chess-results.com/tnr%s.aspx?lan=1&art=0&turdet=YES&flag=30&wi=984&zeilen=99999'

for section in sections:
    print 'Fetching section:', section[1]
    r = requests.get(url % section[0])
    if r.status_code == 200:
        with open('lists/%s.csv' % section[1], 'w') as f:
            writer = csv.writer(f)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.findAll('table', {'class': 'CRs1'})[0]
            for row in table.findAll('tr')[1:]:
		writer.writerow([td.text for td in row])


