import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SPOTIFY_CREDS = {'client_id': os.environ.get('SPOTIFY_CLIENT_ID'), 'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET')}

############################################################################
SPOTIFY_CHARTS = {
    "United States Top 50" : ("spotifycharts", "37i9dQZEVXbLRQDuF5jeBp"),
    "United Kingdom Top 50" : ("spotifycharts", "37i9dQZEVXbLnolsZ8PSNw"),
    "Global Top 50" : ("spotifycharts", "37i9dQZEVXbMDoHDwVN2tF"),
    "United States Viral 50" : ("spotifycharts", "37i9dQZEVXbKuaTI1Z1Afx"),
    "United Kingdom Viral 50" : ("spotifycharts", "37i9dQZEVXbL3DLHfQeDmV"),
    "Global Viral 50" : ("spotifycharts", "37i9dQZEVXbLiRSasKsNU9")
}
SPOTIFY_TRACK_FEATURES = ['artist', 'track', 'album', 'id', 'danceability',
'energy', 'key', 'loudness', 'mode', 'speechiness', 'instrumentalness',
'tempo', 'liveness', 'duration_ms']
############################################################################
