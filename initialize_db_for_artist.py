import sqlite3
import sys

def writeSongs(filename, database, artist):
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    id = 0
    # for each song add it into the db with elo 1000, and 0 appearances
    with open(filename) as songlist:
        for song in songlist:
            song = song.strip()
            song_and_album = song.split(';')
            song = song_and_album[0]
            album = song_and_album[1]
            link = song_and_album[2]
            sql_command = "INSERT INTO "+ artist +" (id, song, album, elo, link, num_shown) VALUES ('"+ str(id)+ "','"+ song +"', '"+ album +"', '"+ str(1000)+ "','"+ link +"', '"+ str(0) +"');"
            cursor.execute(sql_command)
            id += 1
    conn.commit()
    conn.close()


artist = sys.argv[1]

database = "song_rankings.db"
songlist = "song_lists/" + artist + "_song_list.txt"
conn = sqlite3.connect(database)
cursor = conn.cursor()
sql_command = "CREATE TABLE " + artist + " (id int, song varchar(255), album varchar(255), elo int, link varchar(255), num_shown int);"
try:
    cursor.execute(sql_command)
except:
    print("Table already exists in DB, dropping and remaking table, and continuing...")
    cursor.execute("DROP TABLE " + artist + ";")
    cursor.execute(sql_command)
conn.commit()
conn.close()
writeSongs(songlist, database, artist)
