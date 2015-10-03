## WYCC2015 Game Tools

This is a set of simple python scripts that were developed to automate the collection of games for participants in the 2015 World Youth Chess Championships.  They were developed on Linux and OSX, but someone knowledgable could probably make them work on Windows.

### Setup

These scripts are very simple, in part because they rely on a few simple python libraries for HTTP request and HTML parsing.  The necessary libraries are listed in `requirements.txt`.  A common practice is to use `pip` to install `virtualenv` and then use `pip` to install the required packages into the `virtualenv`. On Linux or OSX,
```
sudo easy_install pip
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
On Windows `pip` is usually installed with your Python installation,
```
pip install virualenv
virtualenv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```


### Get Player Lists

The first step is to download up-to-date player lists from the chess-results.com server. The `get_player_lists.py` script performs this task using `requests` to download the raw data and `BeautifulSoup` to scrape the relevant content from the page.  To run this script, simply type:
```
python get_player_lists.py
```
The player lists will be stored in the `lists/` directory in comma-separate value (.csv) files, one per section.  These files are used by the other scripts to lookup player data.

### Download Games from Chess-DB.com

The `download_chess_db_games.py` script uses the player list csv files in the `lists/` directory and the `requests` library to download PGN files from the chess-db.com server.

**NOTE:** Chess-db.com limits the number of PGN files that you can download from their server.  If you are not signed in, the limit is very low (less than 20 players).  To work around this issue:
1. Go to chess-db.com in a normal web browser (I use Chrome).
2. Create an account, if you don't already have one.
3. Login to your account
4. Open the developer console (in Chrome, hit F12)
5. In the developer console, extract the cookie value for `JSESSIONID`.
6. Add the cookie values to the `download_chess_db_games.py` script in the appropriate spot near the top.

Finally, the script can be run as follows:
```
python download_chess_db_games.py
```
The script will process all of the files that match `lists/*.csv` and create corresponding PGN files in the `PGNs/` directory.

### Download TWIC Archives

The _The Week In Chess_ website provides extremely current games from a variety of sources.  Before searching for games for the WYCC participants we download a couple of years worth of games from the TWIC website.  The script is run as follows:
```
python download_twic_archives.py
```
The exact range of weeks you are interested in (948-1090, in my case) can be determined [here](http://theweekinchess.com/twic)

### Extract Games from TWIC Data Set

Once the TWIC games have been downloaded in the step above, you can extract relevant games using the `extract_twic_games.py` script.  Simply run:
```
python extract_twic_games.py
```
The script will process all of the files that match `lists/*.csv` and create corresponding PGN files in the `PGNs/` directory.
