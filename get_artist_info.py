# Imports
import sys
import os
import time
import sqlite3
import spotipy
import string
import urllib.request
from spotipy.oauth2 import SpotifyClientCredentials

"""
USAGE
Just run as python3 get_artist_info.py <artist_spotify_code>
artist spotify code can be found just by copying URI spotify artists page
It will copy as something like spotify:artist:7ITd48RbLVpUfheE7B86o2
just use the ID: for example 7ITd48RbLVpUfheE7B86o2
NOTE: You will also need a spotify API key to use
set environment variables in command line:
  export SPOTIFY_CLIENT_ID=<ID>
  export SPOTIFY_CLIENT_SECRET=<ID>

This will create a txt file in the directory song_lists with the suffix '_new'
This will also create a folder in the images folder with suffix '_new'

This is just to ensure you don't accidentally write over any files you have
manually edited and want to keep. Simply delete the suffixes for full
functionality with the website.
Run initialize_db_for_artist.py once suffixes are removed.
See that file for its usage
"""
def getEmbedUrl(track_id):
    return "https://open.spotify.com/embed/track/" + track_id

def writeArtistName(artist):
    conn = sqlite3.connect('song_rankings.db')
    cursor = conn.cursor()
    artists = cursor.execute("INSERT INTO artist_names (name) VALUES (\'"+artist+"\');")

artist_id = sys.argv[1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# get the list of albums for the artist_id
results = spotify.artist_albums(artist_id, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

# get the artists last name (as artist_tag)
artist = spotify.artist(artist_id)['name']
try:
    writeArtistName(artist)
except:
    print("Wasn't able to add artist name --" + artist + "-- please add manually")
artist_tag = artist.split()[-1].lower()

#make the song_lists directory if none exist
pathname = "song_lists/"
if not os.path.exists(pathname):
    os.makedirs(pathname)

# create and write into the song_list txt file
file = open('song_lists/' + artist_tag + '_song_list_new.txt', 'w+')

# ensure no duplicates are added to the list of songs
songs_added = set()

for album in albums:
    album_uri = album['uri']
    album_name = album['name'].replace("\'", "")

    #get the tracks of the album
    results = spotify.album_tracks(album_uri)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    # write to file track_name;album_name;embed_url
    for track in tracks:
        line_to_write = ""
        track_name = track['name']
        track_name = track_name.replace("\'", "")
        if track_name in songs_added:
            break
        else:
            songs_added.add(track_name)
        embed_url = getEmbedUrl(track['id'])
        line_to_write += track_name + ";" + album_name + ";" + embed_url + "\n"
        file.write(line_to_write)

    # get and download the link to the album art
    album_art_url = album['images'][0]['url']
    album_art_name = album_name.replace(" ", "_").lower()
    pathname = 'static/images/' + artist_tag + '_new/'
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    urllib.request.urlretrieve(album_art_url, 'static/images/' + artist_tag + '_new/' + album_art_name + '.png')

file.close()
