from asyncio import sleep
from flask import Flask, redirect, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import requests
from urllib.parse import urlencode
import base64
import webbrowser
import ticketpy

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('./index.html')

@app.route('/concerts')
def concerts():
   return render_template('./concerts.html')

@app.route('/spotify')
def spotify():

   auth_headers = {
      "client_id": credentials.client_id,
      "response_type": "code",
      "redirect_uri": "http://127.0.0.1:5000/spotify/callback",
      "scope": "user-read-recently-played, user-library-read, user-follow-read, user-top-read"
   }

   # webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

   code = "AQAVZJwC8Et4RYv_dfwPjX8ihaz60joHO7VmdGUGYw-Fzp28Oo5iflD6MO_JZe7YfArRSF4Ji3hE_KHBH5lT_vpO9mKkFMpZuFrtzXNuWK_Bb6PiOfLK56idEP4LgqCYSwGGWVusppKkTgr-hKlwi_Cf2xWv1b4jtPcFXzimgNhsC1Dm2ArwpZ0JhifYUgs7wBN_H_w"
   encoded_credentials = base64.b64encode(credentials.client_id.encode() + b':' + credentials.client_secret.encode()).decode("utf-8")

   token_headers = {
      "Authorization": "Basic " + encoded_credentials,
      "Content-Type": "application/x-www-form-urlencoded"
   }

   token_data = {
      "grant_type": "authorization_code",
      "code": code,
      "redirect_uri": "http://127.0.0.1:5000/callback"
   }

   r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
   
   try:
      token = r.json()["access_token"]
      user_headers = {
      "Authorization": "Bearer " + token,
      "Content-Type": "application/json"
      }

      user_params = {
         "limit": 50
      }

      user_tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", params=user_params, headers=user_headers)

      print(user_tracks_response.json())
   except:
      user_tracks_response = {}

   # Working code here.

   scope = "user-read-recently-played, user-library-read, user-follow-read, user-top-read"
   sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri=credentials.redirect_uri, scope=scope))
   results = {}

   # user info 
   results['current_user'] = sp.current_user()

   # recently played 
   results['current_user_recently_played'] = sp.current_user_recently_played()

   # top tracks 
   results['top_tracks'] = sp.current_user_top_tracks()

   # reccomendations - genres
   results['rec_genre'] = sp.recommendation_genre_seeds()

   return render_template('./spotify_connected.html', results = results)

@app.route('/get_concerts')
def get_concerts():
    
   genre = str(request.args.get('genre'))
   state = str(request.args.get('state'))
   start = str(request.args.get('start'))
   end = str(request.args.get('end'))

   tm_client = ticketpy.ApiClient(credentials.consumer_key)

   # events by genre
   pages = tm_client.events.find(
      classification_name=genre,
      state_code=state,
      start_date_time=start,
      end_date_time=end
   )

   # pages = tm_client.events.find(
   #    classification_name='Pop',
   #    state_code='PA',
   #    start_date_time='2023-05-01T20:00:00Z',
   #    end_date_time='2023-12-01T20:00:00Z'
   # )

   events = []

   for page in pages:
      for event in page:
         try:
            print(event.status)
            events.append(event)

         except:
            break
      break

   return render_template('./concerts.html', events=events)

if __name__ == '__main__':
   app.run()