import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from constants import client_id, client_secret

"""
1. This app asks a user for the date in YYYY-MM-DD format for which he wants to search the top 100 Billboard songs.
2. It then uses BeautifulSoup library to scrape the top 100 songs from https://www.billboard.com/charts/hot-100 and
create a list of these songs (str).
3. It will then authenticate with Spotify using client id and secret and will generate a token and fetch user id. 
4. It will then loop through the list of top 100 BillBoard songs from above and search the URI from spotify for each 
song.
5. It will then create a new Spotify playlist for these songs.

"""

URL = "https://www.billboard.com/charts/hot-100"
user_input = input("Which year you want to travel to? Type the date in format 'YYYY-MM-DD'")

YEAR = user_input.split('-')[0]

print(f'{URL}/{user_input}')
content = requests.get(f'{URL}/{user_input}').text

soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify())

list_of_songs = soup.find_all(name="span",
                              class_="chart-element__information__song text--truncate color--primary")

print(list_of_songs)

songs = [song.getText() for song in list_of_songs]
print(songs)


# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id,
                              client_secret=client_secret,
                              redirect_uri="http://example.com/",
                              scope="playlist-modify-private",
                              show_dialog=True,
                              cache_path="token.txt"
                              )
                    )

user_id = sp.current_user()["id"]
print(user_id)

# Searching for song in Spotify
songs_uri = []
for song in songs:
    q = f"track: {song} year: {YEAR}"
    result = sp.search(q=q, limit=1, type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        print(uri)
        songs_uri.append(uri)
    except IndexError:
        pass

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(songs_uri)


# Creating Spotify playlist
PLAYLIST_NAME = f"{user_input} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=PLAYLIST_NAME, public=False)

# Add songs to playlist
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=songs_uri)
