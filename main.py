import time
from flask import Flask, request, url_for, session, render_template, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from dotenv import load_dotenv
import requests  # Add this import statement

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'abcd123'
TOKEN_INFO = 'token_info'
load_dotenv()

class Artist:
    def __init__(self, name, img_url, albums, tracks, username):
        self.name = name
        self.img_url = img_url
        self.albums = albums
        self.tracks = tracks
        self.username = username

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("No token info")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO] = token_info
    return token_info

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('get_top_artists', _external=True))

@app.route('/get_top_artists')
def get_top_artists():
    try:
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_top_artists(limit=5)
        top_artists = [artist['name'] for artist in results['items']]
        artistIds = [artist['id'] for artist in results['items']]
        userInfo = sp.current_user()
        username = userInfo['id']
        images=[]
        artists = []
        API_KEY = "AIzaSyBJddWSSkt26KMOyxKt0tyTUSdK3e4c3Xs"
        SEARCH_ENGINE='16617c7fb330d4a76'
        count = 0
        for x in top_artists:
            query= x+ " wikipedia"
            url='https://www.googleapis.com/customsearch/v1'
            params={
                'q': query,
                'key':API_KEY,
                'cx':SEARCH_ENGINE,
                'searchType':'image'
            }
            response=requests.get(url,params=params)
            result=response.json()
            artist_id = artistIds[count]
            albums = sp.artist_albums(artist_id, album_type='album', limit=5)
            tempAlbums = []
            for album in albums['items']:
                tempAlbums.append(album['name'])
            top_tracks = sp.artist_top_tracks(artist_id)
            tempTopTracks = []
            for track in top_tracks['tracks'][:5]:
                tempTopTracks.append(track['name'])
            tempStudent = Artist(x, result['items'][0]['link'], tempAlbums, tempTopTracks, username)
            artists.append(tempStudent)
            count+= 1
        return render_template('index.html', artists=artists)
    except Exception as e:
        print("Error:", e)
        return render_template('index.html', artists=[])

def create_spotify_oauth():
    return SpotifyOAuth(
    client_id="a8dd8b7decf845e1b7becdc8dbb909e3",
    client_secret="c6cfafd242384321b9c4aa81b58fb5fd",
    redirect_uri=url_for('redirect_page', _external=True),
    scope='user-top-read'
)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
