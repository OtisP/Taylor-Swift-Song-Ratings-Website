# Imports
import sqlite3
import json
from ranking import elo

# Import Flask
from flask import Flask, render_template
app = Flask(__name__)

# Server routes
# (1) This will return a webpage
@app.route("/")
def get_main_page():
    return render_template("index.html")

# (2) This will return a text response
@app.route('/getsongs/<artist>')
def getsongs(artist):
    # Record search
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    # Get 2 random songs that have shown up the fewest amount of times.
    # There's a +1 to the min, to vary song comparisions a bit
    sql_command = 'SELECT * FROM ' + artist + ' WHERE num_shown<(SELECT min(num_shown) FROM ' + artist + ')+1 ORDER BY RANDOM() LIMIT 2;'
    songs = cursor.execute(sql_command)

    returnable_songs = []
    for song in songs:
        returnable_songs.append(song)
    conn.close()

    return json.dumps(returnable_songs)

# (3) This will return the database info
@app.route('/songrankings/<artist>')
def get_history(artist):
    toReturn = ""
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    historyData = cursor.execute("select * from " + artist + ";")

    toReturn = ""
    for row in historyData:
        for item in row:
            toReturn += str(item) + "|"
        toReturn += "<br>\n"
    conn.close()
    return toReturn

# (4) This will submit the ranking
@app.route('/submitranking/<artist>/<winner_info>')
def submit_ranking(artist, winner_info):
    #parse the input
    print(winner_info)
    winner_info = winner_info.split(',')
    winner_id = int(winner_info[0])
    loser_id = int(winner_info[1])
    kfactor = int(winner_info[2])*3

    #get the elos and times shown from the id's
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()

    sql_command = 'SELECT elo, num_shown FROM ' + artist + ' WHERE id='+ str(winner_id) +';'
    winner_stats = cursor.execute(sql_command)
    for row in winner_stats:
        winner_elo = row[0]
        winner_num_shown = row[1]

    sql_command = 'SELECT elo, num_shown FROM ' + artist + ' WHERE id='+ str(loser_id) +';'
    loser_stats = cursor.execute(sql_command)
    for row in loser_stats:
        loser_elo = row[0]
        loser_num_shown = row[1]

    #calculate the new elos
    new_winner_elo = elo.winnerFirstsNewElo(winner_elo, loser_elo, kfactor)
    new_loser_elo = elo.loserFirstsNewElo(loser_elo, winner_elo, kfactor)

    #write those new elos into the database, and increment times shows
    sql_command = 'UPDATE ' + artist + ' SET elo = '+ str(new_winner_elo) +', num_shown = '+ str(winner_num_shown+1) +' WHERE id = '+ str(winner_id) +';'
    cursor.execute(sql_command)
    sql_command = 'UPDATE ' + artist + ' SET elo = '+ str(new_loser_elo) +', num_shown = '+ str(loser_num_shown+1) +' WHERE id = '+ str(loser_id) +';'
    cursor.execute(sql_command)
    conn.commit()

    conn.close()
    return json.dumps(winner_info)

# (5) This webpage will list the ranking in a pretty way
@app.route("/leaderboard")
def get_leaderboard_page():
    return render_template("leaderboard.html")

# (6) This will return all of the songs/info in order
@app.route("/leaderboard/<artist>")
def get_artist_ranking(artist):
    #build a list of lists, where for each item in the larger list
    #   item 0 is artwork link
    #   item 1 is Rank, just incrementing by one for each song
    #   item 2 is the ELO for the song
    #   item 3 is the song name
    song_info = []
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()

    sql_command = "SELECT album, id, elo, song FROM " + artist + " ORDER BY elo DESC, num_shown DESC, song;"

    leaderboard_song_list = cursor.execute(sql_command)
    conn.close()

    rank = 0
    for row in leaderboard_song_list:
        song = []
        # parse the album into the png needed
        album_name = row[0].lower().replace(" ", "_")
        song.append("/static/images/" + artist + "/" + album_name + ".png")

        rank += 1
        song.append(rank)

        # make the ELO a little more readable
        song.append(round(row[2],2))

        #add in the song name
        song.append(row[3])
        song_info.append(song)
    return json.dumps(song_info)

@app.route("/about")
def get_about_page():
    return render_template("about.html")

@app.route("/get_artists")
def get_artists():
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    artists = cursor.execute("SELECT * FROM artist_names;")

    artist_list = []
    for row in artists:
        artist_list.append(row[0])

    conn.close()
    return json.dumps(artist_list)

@app.route("/get_num_submissions/<artist_tag>")
def get_num_submissions(artist_tag):
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    rows = cursor.execute("SELECT SUM(num_shown) FROM " + artist_tag + ";")
    for row in rows:
        num_shown_total = row[0]
    conn.close()

    num_submissions = int(num_shown_total)//2
    return str(num_submissions)

if __name__ == '__main__':
    app.run()
