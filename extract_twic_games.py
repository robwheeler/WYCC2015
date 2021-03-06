#! /usr/bin/env python
from __future__ import print_function
import os
import glob
import csv
import pgn
from collections import defaultdict

interesting = {}
outfiles = []
found = set()
directory = {}
section_set = defaultdict(set)

# Read in all of the players, their FIDE IDs, and their section
# Create an open file handle for each section
for filename in glob.glob(os.path.join('lists', '*.csv')):
    section = os.path.splitext(os.path.basename(filename))[0]
    outfile = open(os.path.join('PGNs', 'TWIC_{}.pgn'.format(section)), 'w')
    outfiles.append(outfile)
    with open(filename) as infile:
        reader = csv.reader(infile)
        for row in reader:
            interesting[row[4]] = outfile
            directory[row[4]] = (section, row[3])
            section_set[section].add(row[4])


# Sort the twic files numerically so that the games appear
# in chronological order in the output files
def twic_key(a):
    return int(os.path.splitext(os.path.basename(a))[0][len('twic'):])

# Loop over all TWIC games, finding the interesting ones
# and adding them to the appropriate output file(s)
for pgn_filename in sorted(glob.glob(os.path.join('twic', '*pgn')), key=twic_key):
    print(pgn_filename)
    games = pgn.loads(open(pgn_filename).read())
    for game in games:
        white_id = getattr(game, 'whitefideid', None)
        black_id = getattr(game, 'blackfideid', None)
        white_file = interesting.get(white_id)
        black_file = interesting.get(black_id)
        if white_file:
            found.add(white_id)
            print('Found game {} in {}'.format(game, pgn_filename))
            print(game.dumps() + '\n\n', file=white_file)
        if black_file and black_file != white_file:
            found.add(black_id)
            print('Found game {} in {}'.format(game, pgn_filename))
            print(game.dumps() + '\n\n', file=black_file)

# Come up with some stats on how well "covered" the field is
missing_set = set(interesting.keys()) - found
missing_list = defaultdict(list)

for player in missing_set:
    section, name = directory[player]
    missing_list[section].append((player, name))

for section in sorted(missing_list.keys()):
    missing = len(missing_list[section])
    total = len(section_set[section])
    print('{}: Found {} / {} (:.2f%%)'.format(section, total - missing, total, (100. * (total - missing) / total)))

# List the players that were missed in the TWIC games
for section in sorted(missing_list.keys()):
    print('Missing for:', section)
    for player in missing_list[section]:
        print(player)
    print()
