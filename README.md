# kshe-to-spotify

As a big fan of Classic Rock living in France, I am very frustrated by the
lack of good classic rock radio we have. I spent four months in St Louis, MO,
and I had the chance to listen to [KSHE 95](http://www.kshe95.com/) every day,
playing some of my favorite classic rock tunes. Unfortunately, I can't listen
to this radio in France as they block it. Fortunately, their website shows
the tunes [currently playing](http://player.listenlive.co/20101/en/songhistory)
, as well as a few previous ones. I decided to scrap this page, make myself
an empty [Spotify playlist](https://open.spotify.com/user/ericda/playlist/3BCcE8T945z1MnfPWkFsfX),
and automatically add in the KSHE tracks.

So far, I am able to:

- Scrap KSHE's web page, and get a list of 10 songs they've played
- Find the songs on Spotify thanks to their web API
- Upload them to a playlist I created, making sure there is no duplicate

My next steps include:

- Automate this with a cron (or use something smarter like Airflow)
  so the playlist keeps getting updated
- Pull some stats about what's playing, and when, trying to predict
  the next song, or mood, who knows what ...

Feel free to ping me if you want to help!

## Installation

To make it work, here's what to do.

First, you'll need to setup your Spotify developer account, and register an app.
Find how [here](https://developer.spotify.com/web-api/).
Once your app is created, you will have access to the following crendentials:

- client_id
- client_secret
- redirect_uri

The app will need those to update tracks to your playlist.
Copy the file ```.spotify-token.json.dist``` into ```.spotify-token.json```
and fill in these credentials. You will also need your spotify *user-id*
(your username) and the *playlist-uri* to which you'll upload the tracks to.

Once you're good, follow these commands to start the server.

``` shell
git clone https://github.com/ericdaat/kshe-to-spotify.git
cd kshe-to-spotify
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd flask-server
uwsgi wsgi.ini
```

The app should now be running on ```localhost:9999```.

## API

The calls supported so far are:

- [GET] ```localhost:9999/```: Doesn't do much
- [GET] ```localhost:9999/auth```: Authenticate for 3600 seconds
- [POST] ```localhost:9999/update_playlist```: Updates the playlist with the latest songs
