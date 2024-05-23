import requests
import time
from flask import Flask, request, url_for, session,render_template, redirect
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv

app = Flask(__name__)
#creating a temp cookie to load faster

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
#creating a dummy key to access
app.secret_key = 'abcd123'
#authentication token 
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
    #if theres no token or 60 seconds past before token refresh ti and send it
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
     #calling the authorization function 
    auth_url = create_spotify_oauth().get_authorize_url()
     #this will retunr the url for it 
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    # Requesting the actual token under
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('get_top_artists', _external=True))


@app.route('/get_top_artists')
def get_top_artists():
    try:
        #using token to get acces
        token_info = get_token()
        #use spotipy spotify api to access the account
        sp = spotipy.Spotify(auth=token_info['access_token'])
        #api documentation for top artist only grabbing the 4
        results = sp.current_user_top_artists(limit=5)
        
        #lc for getting the artist in the top artiist
        top_artists = [artist['name'] for artist in results['items']]
        artistIds = [artist['id'] for artist in results['items']]
        
        #username 
        #user info
        userInfo = sp.current_user()
        username = userInfo['id']

        #printing the array of top artist
        #hometown 
        images=[]
        artists = []
        #google search api key
        API_KEY= os.getenv('API_KEY')
        #search engine api key
        SEARCH_ENGINE='16617c7fb330d4a76'
        #for loop on top artist 
        count = 0
        for x in top_artists:
            # the actual search we put into the api
            query= x+ " wikipedia"
            #url access to the api
            url='https://www.googleapis.com/customsearch/v1'
            params={
                #search
                'q': query,
                #key bs
                'key':API_KEY,
                'cx':SEARCH_ENGINE,
                'searchType':'image'
        }
            #request the api with the current search paramets
            response=requests.get(url,params=params)
            #gets the result from the request
            result=response.json()

            #get artist most recent albums
            artist_id = artistIds[count]
            albums = sp.artist_albums(artist_id, album_type='album', limit=5)
            tempAlbums = []
            for album in albums['items']:
                tempAlbums.append(album['name'])

            #tracks
            top_tracks = sp.artist_top_tracks(artist_id)
            tempTopTracks = []
            for track in top_tracks['tracks'][:5]:
                tempTopTracks.append(track['name'])
            

            #create the class  for this specific artist and add it to the array of artists
            tempStudent = Artist(x, result['items'][0]['link'], tempAlbums, tempTopTracks, username)
            artists.append(tempStudent)
            
            #increase count for the albums
            count+= 1

        return render_template('index.html', artists=artists)
    except Exception as e:
        print("Error:", e)
        #if you want to run it so it works remove everthing and return images
        return render_template('index.html', artists=[])
        


def create_spotify_oauth():
    return SpotifyOAuth(
        #the BS from the actual api dashboard info
        client_id=os.getenv('client_id'),
        client_secret=os.getenv('client_secret'),
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-top-read'
    )

 

if __name__ == '__main__':
    #fix the host and port issues so it works  on other users computers
    #deploy on the interentt
    #do a gitpull a run locally
    #implement database logic mongodb or sqL
    app.run(debug=True, port=5000, host='0.0.0.0')