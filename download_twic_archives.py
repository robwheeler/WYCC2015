#!/usr/bin/env python
# This script courtesy of Ludmila Bashkansky
from __future__ import print_function
import requests
import zipfile
import StringIO


for issue in xrange(948, 1091):
    print('Downloading issue:', issue)
    url = "http://www.theweekinchess.com/zips/twic{}g.zip".format(issue)
    r = requests.get(url)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall("twic")
