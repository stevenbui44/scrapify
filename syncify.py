import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import time
import requests
from urllib.parse import urlencode
from spotipy.cache_handler import CacheHandler

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
class NoCache(CacheHandler):
    def get_cached_token(self):
        return None

    def save_token_to_cache(self, token_info):
        pass

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_handler=NoCache()
    )

@app.route('/')
def index():
    sp_oauth = create_spotify_oauth()
    
    # Check if the user has just logged out
    logout_message = None
    if request.args.get('logout') == 'success':
        logout_message = "You have been successfully logged out."
    
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url()
        return render_template('index.html', auth_url=auth_url, message=logout_message)
    
    return redirect(url_for('choose_playlists'))
    

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('choose_playlists'))


@app.route('/privacy-policy')
def privacy_policy():
    # return render_template('privacy_policy.html')
    is_logged_in = 'token_info' in session
    return render_template('privacy_policy.html', is_logged_in=is_logged_in)


@app.route('/about')
def about():
    # return render_template('about.html')
    is_logged_in = 'token_info' in session
    return render_template('about.html', is_logged_in=is_logged_in)


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    
    # Redirect to the index page with a logout success message
    return redirect(url_for('index', logout='success'))


@app.route('/choose-playlists')
def choose_playlists():
    if not session.get('token_info'):
        return redirect(url_for('index'))
    
    try:
        sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
        
        # Fetch all playlists
        all_playlists = []
        offset = 0
        limit = 50  # Spotify API default limit

        while True:
            playlists = sp.current_user_playlists(limit=limit, offset=offset)
            all_playlists.extend(playlists['items'])
            
            if len(playlists['items']) < limit:
                # We've reached the end of the playlist list
                break
            
            offset += limit

        return render_template('choose_playlists.html', playlists=all_playlists)
    except spotipy.exceptions.SpotifyException:
        # Token might have expired
        session.pop('token_info', None)
        return redirect(url_for('index'))
    

@app.route('/playlist-created', methods=['POST'])
def create_playlist():
    if not session.get('token_info'):
        return redirect(url_for('index'))
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    selected_playlists = request.form.getlist('playlists')
    include_duplicates = 'include_duplicates' in request.form
    all_tracks = []
    selected_playlist_names = []

    for playlist_id in selected_playlists:
        playlist = sp.playlist(playlist_id)
        selected_playlist_names.append(playlist['name'])
        tracks = []
        results = sp.playlist_items(playlist_id)
        tracks.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        all_tracks.extend([(track['track']['id'], track['added_at'], track['track']['name'], playlist['name']) 
                           for track in tracks if track['track']])

    # Sort tracks by added_at date
    sorted_tracks = sorted(all_tracks, key=lambda x: datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%SZ'))

    if not include_duplicates:
        # Remove duplicates if not including them
        unique_tracks = []
        seen = set()
        for track in sorted_tracks:
            if track[0] not in seen:
                unique_tracks.append(track)
                seen.add(track[0])
        sorted_tracks = unique_tracks

    # Create the description
    if len(selected_playlist_names) == 1:
        description = f"Combined playlist from {selected_playlist_names[0]}, sorted by add date"
    elif len(selected_playlist_names) == 2:
        description = f"Combined playlist from {selected_playlist_names[0]} and {selected_playlist_names[1]}, sorted by add date"
    else:
        description = "Combined playlist from "
        for i, name in enumerate(selected_playlist_names):
            if i == len(selected_playlist_names) - 1:
                description += f"and {name}, "
            else:
                description += f"{name}, "
        description += "sorted by add date"

    # Truncate the description if it's too long (Spotify has a 300 character limit)
    if len(description) > 300:
        description = description[:297] + "..."

    # Create a new playlist
    user_id = sp.me()['id']
    new_playlist = sp.user_playlist_create(user_id, "Combined Playlist", public=True, 
                                           description=description)

    # Add tracks to the new playlist in batches of 100
    track_ids = [track[0] for track in sorted_tracks]
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        try:
            sp.playlist_add_items(new_playlist['id'], batch)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error adding tracks {i} to {i+100}: {str(e)}")
        time.sleep(1)  # Add a small delay to avoid rate limiting

    return render_template('playlist_created.html', playlist_name=new_playlist['name'], tracks=sorted_tracks)


if __name__ == '__main__':
    app.run(debug=True, port=5001)