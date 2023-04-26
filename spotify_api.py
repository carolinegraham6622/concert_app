import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials

# scope = "user-read-recently-played"
scope = "user-read-recently-played, user-library-read, user-follow-read, user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=credentials.redirect_url, scope=scope))

# --
# personalized spotify stats 
# --

# user info 
currernt_user = sp.current_user()
print(currernt_user)

# recently played 
results = sp.current_user_recently_played()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " by ", track['name'])

# top tracks 
top_tracks = sp.current_user_top_tracks()
for track in top_tracks['items']:
    print(track['name'])

# reccomendations - genres 
results = sp.recommendation_genre_seeds()
for r in results:
    print(results[r])


# can use this for more general front page ? like a dropdown 
# category_playlists(category_id=None, country=None, limit=20, offset=0)

# TODO: add a return statement ... 