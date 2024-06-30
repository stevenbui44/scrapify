import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for, session

# Load environment variables
load_dotenv()

# Set up your credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-read-private'

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

@app.route('/analyze/<playlist_id>')
def analyze_playlist(playlist_id):
    if not session.get('token_info'):
        return redirect(url_for('index'))
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlist = sp.playlist(playlist_id)
    tracks = sp.playlist_items(playlist_id)
    return render_template('analyze.html', playlist=playlist, tracks=tracks['items'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
