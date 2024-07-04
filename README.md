# Syncify

Syncify is a web application that allows Spotify users to combine multiple playlists into one, sorted by the date each song was added. This tool simplifies playlist management and helps users rediscover songs they've added over time across different playlists, as well as to keep all of your favorite songs in one place.

## Features

- Combine multiple Spotify playlists into one
- Sort combined playlist by date added
- Option to include or exclude duplicate songs
- Seamless integration with Spotify accounts
- User-friendly interface

## Tech Stack

- Backend: Python with Flask framework
- Frontend: HTML, CSS, JavaScript
- Spotify API Integration: Spotipy library

## Installation

1. Clone the repository:
```
git clone https://github.com/stevenbui44/syncify.git
```
2. Install required dependencies:
```
pip install -r requirements.txt
```
3. Set up a [Spotify for Developers](https://developer.spotify.com/) account
5. Create an app to get your client ID and client secret
6. Create a new .env file
7. Add your Spotify credentials into the .env file:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=your_redirect_uri
```
7. Run the application:
```
python syncify.py
```

## Usage

1. Open the application in localhost:5001
<img width="1438" alt="image" src="https://github.com/stevenbui44/syncify/assets/140114252/67581717-aad0-476c-b28d-b1ef8ea0f644">
2. Log in with Spotify credentials
