# Import necessary libraries
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Authentication
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_id_from_url(url):
    return url.split("/")[-1].split("?")[0]

def recommend_from_playlist(playlist):
    if "spotify.com" in playlist:
        playlist_id = get_playlist_id_from_url(playlist)
    else:
        playlist_id = playlist

    try:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        seed_track_ids = [
            track['track']['id'] for track in playlist_tracks['items'][:5]
        ]

        recommendations = sp.recommendations(seed_tracks=seed_track_ids, limit=10)

        print("Recommendations based on the playlist:")
        for track in recommendations['tracks']:
            print(f"{track['name']} by {track['artists'][0]['name']}")
    except Exception as e:
        print(f"An error occurred: {e}")

def recommend_from_song(track_name):
    results = sp.search(q=track_name, type='track', limit=1)

    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        
        print(f"Recommendations for '{track_name}':")
        for track in recommendations['tracks']:
            print(f"{track['name']} by {track['artists'][0]['name']}")
    else:
        print(f"No tracks found for '{track_name}'")
cmd = ''
while cmd not in ["0", "leave", "exit"]:
    cmd = input("From a playlist or song? ")
    if cmd.lower() == 'playlist':
        playlist_url_or_id = input("Enter the Spotify playlist URL or ID: ")
        recommend_from_playlist(playlist_url_or_id)
    if cmd.lower() == 'song':
        track_name = input("Enter a song name: ")
        recommend_from_song(track_name)
    elif cmd not in ["0", "leave", "exit"]:
        print('nice try buddy')