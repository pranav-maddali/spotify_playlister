# Spotify Playlister

A web app designed to cluster tracks from the top charts on Spotify using DBSCAN and PCA. 
***
## Tools Used:
- Flask
- Heroku
- Flask-SQLAlchemy
## Languages Used:
- Python
- JavaScript
- HTML/CSS
***
### Currently in deployment stage with features such as:
1. Saving created playlists to user
2. Exporting playlists to user's spotify

coming soon.
***

If you want to run locally (excluding the user login features):
```
git clone https://github.com/pranav-maddali/spotify_playlister
```
```
pip install requirements.txt
```
```
export FLASK_RUN=app
export FLASK_DEBUG=1
```
```
python3
>>> from app import db, application
>>> db.create_all(app=application)
>>> quit()
```
```
flask run
```
The app should return a table displaying information about the tracks that were clustered.
