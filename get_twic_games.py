#! /usr/bin/env python
import os
import csv
import pgn
from collections import defaultdict

interesting = {}
outfiles = []
found = set()
directory = {}
section_set = defaultdict(set)

def twic_key(a):
    return int(a.split('.')[0][4:])

for filename in os.listdir('lists/'):
    s = filename.split('.')[0].replace(' ', '_')
    outfile = open('PGNs/TWIC_%s.pgn' % s, 'w')
    outfiles.append(outfile)
    with open(os.path.join('lists', filename)) as infile:
        reader = csv.reader(infile)
        for row in reader:
            interesting[row[4]] = outfile
            directory[row[4]] = (s, row[3])
            section_set[s].add(row[4])

for pgn_filename in sorted(os.listdir('twic/'), key=twic_key):
    print pgn_filename
    games = pgn.loads(open(os.path.join('twic', pgn_filename)).read())
    for game in games:
        white_id = getattr(game, 'whitefideid', None)
        black_id = getattr(game, 'blackfideid', None)
        white_file = interesting.get(white_id)
        black_file = interesting.get(black_id)
        if white_file:
            found.add(white_id)
            print 'Found game %s in %s' % (game, pgn_filename)
            print >> white_file, game.dumps() + '\n\n'
        if black_file and black_file != white_file:
            found.add(black_id)
            print 'Found game %s in %s' % (game, pgn_filename)
            print >> black_file, game.dumps() + '\n\n'

missing_set = set(interesting.keys()) - found
missing_list = defaultdict(list)

for player in missing_set:
    section, name = directory[player]
    missing_list[section].append((player, name))

for section in sorted(missing_list.keys()):
    missing = len(missing_list[section])
    total = len(section_set[section])
    print '%s: Found %d / %d (%.2f%%)' % (section, total - missing, total, (100. * (total - missing) / total))

for section in sorted(missing_list.keys()):
    print 'Missing for:', section
    for player in missing_list[section]:
        print player
    print
