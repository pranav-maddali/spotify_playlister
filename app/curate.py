import pandas as pd
import numpy as np
import json

from app.config import *

from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

############################################################################
charts = {
    "United States Top 50" : ("spotifycharts", "37i9dQZEVXbLRQDuF5jeBp"),
    "United Kingdom Top 50" : ("spotifycharts", "37i9dQZEVXbLnolsZ8PSNw"),
    "Global Top 50" : ("spotifycharts", "37i9dQZEVXbMDoHDwVN2tF"),
    "United States Viral 50" : ("spotifycharts", "37i9dQZEVXbKuaTI1Z1Afx"),
    "United Kingdom Viral 50" : ("spotifycharts", "37i9dQZEVXbL3DLHfQeDmV"),
    "Global Viral 50" : ("spotifycharts", "37i9dQZEVXbLiRSasKsNU9")
}
track_features = ['artist', 'track', 'album', 'id', 'danceability',
'energy', 'key', 'loudness', 'mode', 'speechiness', 'instrumentalness',
'tempo', 'liveness', 'duration_ms']
############################################################################

def generateToken():
    #global var for the auth token
    global sp

    #allow us access to Spotify's records
    token = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    cache_token = token.get_access_token()

    sp = spotipy.Spotify(cache_token)

def playlist(username, id_):
    #create a dataframe to store all our tracks
    df = pd.DataFrame(columns=track_features)

    #call the API to return a playlist (in our case, top 50 charts)
    playlist = sp.user_playlist_tracks(username, id_)

    #as shown above, we need to extract the information from items
    tracks = playlist["items"]

    for track in tracks:
        features = {}

        #navigating through the output from the spotify API and gathering categorical data for each track
        features['track'] = track['track']['name']
        features['album'] = track['track']['album']['name']
        features['artist'] = track['track']['album']['artists'][0]['name']
        features['id'] = track['track']['id']

        #we want audio (mostly numerical) data for each track
        audio = sp.audio_features(features['id'])[0]
        #the audio features of each track
        audio_features = ['danceability', 'energy', 'key', 'loudness',
                          'mode', 'speechiness', 'instrumentalness',
                          'tempo', 'liveness', 'duration_ms']

        for feature in audio_features:
            features[feature] = audio[feature]

        #concat each track's dataframe with the overall playlist dataframe
        temp_df = pd.DataFrame(features, index=[0])
        df = pd.concat([df, temp_df], ignore_index=True)

    return df

def playlists(playlist_dictionary):
    output = pd.DataFrame(columns=track_features)

    for (k, v) in playlist_dictionary.items():
        df = playlist(v[0], v[1])

        output = pd.concat([output, df], ignore_index=True)

    return output

def clean():
    all_tracks = playlists(charts)
    all_tracks = all_tracks.drop_duplicates(subset='track', keep='first')

    top5_artists = all_tracks['artist'].value_counts()[:5]

    return all_tracks, top5_artists

def preprocess(tracks):
    X = tracks[tracks.columns[4:]]
    X = StandardScaler().fit_transform(X)

    pca = PCA(n_components=2)
    pC = pca.fit_transform(X)

    pDF = pd.DataFrame(data=pC, columns=['PC1', 'PC2'])

    return pDF

def clustering(dataframe, min_number):
    dbs = DBSCAN(min_samples=min_number)
    dbs.fit(dataframe[['PC1', 'PC2']])

    dataframe['dbscan label'] = np.array(dbs.labels_)
    dataframe = dataframe[dataframe['dbscan label'] != -1]

    labels = dataframe['dbscan label']
    clusters = len(set(labels)) - (1 if -1 in labels else 0)

    return dataframe, clusters

def output(dataframe, all_tracks):
    res = pd.concat([dataframe, all_tracks[all_tracks.columns[:4]]], axis=1)

    res.dropna(inplace=True)
    res.drop(res.columns[:2], axis=1, inplace=True)
    res.sort_values(by=['dbscan label'], ascending=True, inplace=True)

    res['dbscan label'] = res['dbscan label'].apply(lambda x: int(x+1))

    res.rename({'dbscan label':'Playlist #'}, axis=1, inplace=True)

    return res

################################################################################

def create_playlists(tracks_per_cluster):
    generateToken()

    tracks, top_artists = clean()

    processed_DF = preprocess(tracks)
    clustered_DF, clusters = clustering(processed_DF, tracks_per_cluster)

    out = output(clustered_DF, tracks)
    out.reset_index(drop=True, inplace=True)
    out.index = np.arange(1, len(out)+1)

    return out, clusters

################################################################################
