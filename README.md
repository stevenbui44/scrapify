# Syncify

Syncify is a web application that allows Spotify users to combine multiple playlists into one, sorted by the date each song was added. This tool simplifies playlist management and helps users rediscover songs they've added over time across different playlists, as well as to keep all of your favorite songs in one place.

## Features

- **User Authentication**: Secure login using Spotify's OAuth 2.0 protocol
- **Spotify API Integration**: Retrieves and posts playlists using Spotipy library
- **Sorted Playlist Combination**: Combines Spotify multiple playlists into one, with songs sorted by added date
- **User-friendly Interface**: Clean, intuitive design in an organized grid format that adapts to different screen sizes
- **Privacy Policy**: Full disclosure of user data usage

## Tech Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **API**: Spotify API, integrated with Spotipy library

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
<img width="1440" alt="image" src="https://github.com/stevenbui44/syncify/assets/140114252/519f960e-10c0-486f-81d2-cf788e0ee6b5">

2. Log in with Spotify credentials

3. Select playlists to combine
<img width="1440" alt="image" src="https://github.com/stevenbui44/syncify/assets/140114252/0b93ce21-fa1c-440f-b73d-3509d4b6f358">

4. Press Create Playlist
<img width="1440" alt="image" src="https://github.com/stevenbui44/syncify/assets/140114252/ffa02fae-691a-45f5-95c4-53ad5856041d">

5. Enjoy your new playlist B)
<img width="1440" alt="image" src="https://github.com/stevenbui44/syncify/assets/140114252/6c280f4c-8e2d-4a6d-9605-57a7dc11efc6">
