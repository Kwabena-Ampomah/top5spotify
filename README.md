# top5spotify
This project is a Spotify Web Application that uses [Flask](https://flask.palletsprojects.com/en/3.0.x/), [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/), [Bootstrap](https://getbootstrap.com/), Python, HTML, and CSS.

The project will give the user an overview of their favorite artists and some information about them!

Begin by cloning the github repository. Then do the following steps!

## Installing Packages

To use our project you must do the following. In the project directory, you can run:

### `pip install Flask Flask-SQLAlchemy requests spotipy python-dotenv virtualenv`

This installs all of the packages needed.

## Setting up the Application

First, you need to start the environment and the flask application:

```
virtualenv env
source env/bin/activate
export FLASK_APP=main
```

If we decide to commit our API keys to the GitHub repository then this step will not be necessary:

Create a file called .env and fill it with the following variables:

```
API_KEY = "AIzaSyBJddWSSkt26KMOyxKt0tyTUSdK3e4c3Xs"
client_id = "a8dd8b7decf845e1b7becdc8dbb909e3"
client_secret = "c6cfafd242384321b9c4aa81b58fb5fd”
```

Fill these with your respective API keys.
\
\
The API_KEY variable corresponds to your Google Custom Search JSON API Key. This can be found here: [link](https://developers.google.com/custom-search/v1/introduction). Click on the "Get a Key" button.
\
\
The other two variables are for the spotify API. Getting your access tokens are here: [link](https://developer.spotify.com/documentation/web-api/tutorials/getting-started).

## Running the Application

To run the application simply type

### `flask run`

into the console and it should bring you to our webpage!

## Other Helpful Things

If you would like to add your own code to our program the following commands might be helpful! You can run these in your terminal:

```
    FLASK_APP=development #enables debug mode

    kill -9 $(lsof -i :5000 -t) #run after each run of the application to close the ports

```

Also, whenever you run this applciation it will create a file called .cache which you are going to want to delete each time. If you have this file and try to let a new person use the applciation it will still show your results.

