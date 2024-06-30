import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# credentials (inside .env)
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-read-private'

# set up SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

def get_user_playlists():
    playlists = sp.current_user_playlists()
    return [(playlist['name'], playlist['id']) for playlist in playlists['items']]

def analyze_playlist(playlist_id):
    results = sp.playlist_items(playlist_id)
    
    print(f"\nAnalyzing playlist: {sp.playlist(playlist_id)['name']}\n")
    
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
        print(f"   Added at: {item['added_at']}")
        print()

    while results['next']:
        results = sp.next(results)
        for idx, item in enumerate(results['items'], start=len(results['items'])):
            track = item['track']
            print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
            print(f"   Added at: {item['added_at']}")
            print()

# Get user's playlists
user_playlists = get_user_playlists()

# Display playlists
print("Your playlists:")
for idx, (name, _) in enumerate(user_playlists):
    print(f"{idx + 1}. {name}")

# Let user choose a playlist
while True:
    choice = input("\nEnter the number of the playlist you want to analyze (or 'q' to quit): ")
    if choice.lower() == 'q':
        break
    try:
        playlist_index = int(choice) - 1
        if 0 <= playlist_index < len(user_playlists):
            _, playlist_id = user_playlists[playlist_index]
            analyze_playlist(playlist_id)
        else:
            print("Invalid playlist number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")