import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up your credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-read-private playlist-modify-public user-library-read'

# Set up Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Set up SpotifyOAuth
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )

@app.route('/')
def index():
    sp_oauth = create_spotify_oauth()
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlists = sp.current_user_playlists()
    return render_template('index.html', playlists=playlists['items'])

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if not session.get('token_info'):
        return redirect(url_for('index'))
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    selected_playlists = request.form.getlist('playlists')
    all_tracks = []

    for playlist_id in selected_playlists:
        tracks = sp.playlist_items(playlist_id)
        all_tracks.extend([(track['track']['id'], track['added_at'], track['track']['name']) for track in tracks['items']])

    # Sort tracks by added_at date and remove duplicates
    sorted_tracks = sorted(all_tracks, key=lambda x: datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%SZ'))
    unique_tracks = []
    seen = set()
    for track in sorted_tracks:
        if track[0] not in seen:
            unique_tracks.append(track)
            seen.add(track[0])

    # Create a new playlist
    user_id = sp.me()['id']
    new_playlist = sp.user_playlist_create(user_id, "Combined Playlist", public=True, description="Combined playlist sorted by add date")

    # Add tracks to the new playlist in batches of 100
    track_ids = [track[0] for track in unique_tracks]
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        sp.playlist_add_items(new_playlist['id'], batch)

    return render_template('playlist_created.html', playlist_name=new_playlist['name'], tracks=unique_tracks)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
