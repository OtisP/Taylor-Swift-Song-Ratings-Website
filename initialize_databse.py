import sqlite3

def writeSongs(filename, database):
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()

    with open(filename) as songlist:
        for song in songlist:
            song = song.strip()
            song_and_album = song.split(';')
            song = song_and_album[0]
            album = song_and_album[1]
            sql_command = "INSERT INTO songs (song, album, elo, num_shown) VALUES ('"+ song +"', '"+ album +"', '"+ str(1000)+ "', '"+ str(0)+"');"
            cursor.execute(sql_command)
            conn.commit()

    conn.close()

database = "song_rankings.db"
songlist = "song_list.txt"
conn = sqlite3.connect(database)
cursor = conn.cursor()
sql_command = 'CREATE TABLE songs (song varchar(255), album varchar(255), elo int, num_shown int);'
try:
    cursor.execute(sql_command)
except:
    print("Table already exists in DB, continuing")
conn.commit()
conn.close()
writeSongs(songlist, database)
