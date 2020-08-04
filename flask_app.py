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
    # There's a +5 to the min, to vary song comparisions a bit
    sql_command = 'SELECT * FROM ' + artist + ' WHERE num_shown<(SELECT min(num_shown) FROM ' + artist + ')+5 ORDER BY RANDOM() LIMIT 2;'
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

# (5) This website will list the ranking in a pretty way
@app.route("/ranking/<artist>")
def get_ranking_page(artist):
    pass

if __name__ == '__main__':
    app.run()
