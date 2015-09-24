Directory to store games downloaded from TWIC

To populate this directory run something like the following:

`let x=948; while [[ $x -lt 1090 ]]; do echo $x; curl http://www.theweekinchess.com/zips/twic${x}g.zip | funzip > twic${x}.pgn; let x=$x+1; done`
