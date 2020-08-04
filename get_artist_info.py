import sys
import time
import spotipy
import string
from spotipy.oauth2 import SpotifyClientCredentials


def get_embed_url(track_id):
    return "https://open.spotify.com/embed/track/" + track_id

artist_id = sys.argv[1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# get the list of albums for the artist_id
results = spotify.artist_albums(artist_id, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

album_uris = []

# get the artists last name (as artist_tag)
artist = spotify.artist(artist_id)['name']
artist_tag = artist.split()[-1].lower()

# create and write into the song_list txt file
file = open('song_lists/' + artist_tag + '_song_list_new.txt', 'w+')
for album in albums:
    album_uri = album['uri']
    album_name = album['name']

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
        embed_url = get_embed_url(track['id'])
        line_to_write += track_name + ";" + album_name + ";" + embed_url + "\n"
        file.write(line_to_write)

    # get and save the link to the album art
    # TODO:
    # album_art_url = album['images'][0]
    # album_art_name = album_name.replace(" ", "_").lower()
    # art_file = open('static/images/' + artist_tag + '/' + album_art_name + '.txt')
    # art_file.write(album_art_url)
    # art_file.close()


file.close()
