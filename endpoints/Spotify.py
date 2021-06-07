import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
scope = "user-read-currently-playing user-modify-playback-state user-library-modify playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private"

token = util.prompt_for_user_token(
    "jacklaxjk", scope, redirect_uri="http://localhost:8000"
)
