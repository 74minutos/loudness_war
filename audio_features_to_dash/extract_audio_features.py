#we are going to use spotipy to make the API calls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#this are spotify tokens. You need an account to get them:
cid ="XXXXXX"
secret = "XXXXXX"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
SP = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

In [2]:

# timeit library to measure the time needed to run this code
import timeit
start = timeit.default_timer()

DECADES = ['year:1960-1969',
    'year:1970-1979',
    'year:1980-1989',
    'year:1990-1999',
    'year:2000-2009',
    'year:2010-2019']

def make_track(track_name, track_id, album_name, artist_name, popularity, decade):
    return {
        'track_name': track_name,
        'track_id': track_id,
        'album_name': album_name,
        'artist_name': artist_name,
        'popularity': popularity,
        'decade': decade
    }

TRACKS = []

def get_first_year_from_decade(decade):
    span = decade.split(':')[1]
    first_year, last_year = span.split('-')
    return first_year

## Manual unit test
assert '1970' == get_first_year_from_decade('year:1970-1979'), "failed to extract first year: expected 1970"


def get_tracks(decade, spotify_api):
    tracks = []

    year = get_first_year_from_decade(decade)
    ## we expect the year to be an integer
    int(year)
    ## we expect the year to have 4 digits
    assert len(year) == 4

    for i in range(0,2000, 50):
        track_results = spotify_api.search(q=decade, type='track', limit=50, offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            track = make_track(
                track_name =t['name'],
                track_id = t['id'],
                album_name = t['album']['name'],
                artist_name = t['artists'][0]['name'],
                popularity = t['popularity'],
                decade = year)
            tracks.append(track)
    return tracks

for decade in DECADES:
    tracks = get_tracks(decade, SP)
    TRACKS.extend(tracks)



stop = timeit.default_timer()
print ('Time to run this code (in seconds):', stop - start)

import pandas as pd

df_tracks = pd.DataFrame.from_records(TRACKS)

def get_audio_features(track_ids, spotify_api):
    all_audio_features = []
    for track_id in track_ids:
        spotify_audio_features = spotify_api.audio_features([track_id])[0]
        all_audio_features.append(spotify_audio_features)
    return all_audio_features

tracks_audio_features = get_audio_features(df_tracks['track_id'], SP)

df_tracks_audio_features = pd.DataFrame(tracks_audio_features)
df_tracks_audio_features.rename(columns={'id':'track_id'}, inplace=True)
tracks_with_audio_features = pd.merge(df_tracks, df_tracks_audio_features, how='inner', on='track_id')

import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt
loudness = tracks_with_audio_features[['decade', 'loudness']]



#we start here individual audio analysis
def get_audio_analysis(track_id, track_name, spotify_api):
    spotify_audio_analysis = spotify_api.audio_analysis(track_id)
    spotify_audio_analysis_results = pd.DataFrame(spotify_audio_analysis['segments'])
    return(spotify_audio_analysis_results)



import pandas as pd
tracks_names = ['Fortunate_Son', 'Stairway_to_Heaven','Wish You Were Here', 'The Ancient Ones', 'We ll Burn the Sky']
tracks_ids = ['4BP3uh0hFLFRb5cjsgLqDh', '51pQ7vY7WXzxskwloaeqyj', '6mFkJmJqdDVQ1REhVfGgd1', '38Ql1hgcSxnWwzgM40INI1', '6bMNWDLUbJYoKJhFN5OZX8']
TRACKS_FOR_AUDIO_ANALYSIS = pd.DataFrame(list(zip(tracks_names, tracks_ids)), columns=['tracks_names', 'tracks_ids'])

import matplotlib.pyplot as plt
for track, item in TRACKS_FOR_AUDIO_ANALYSIS.iterrows():
    spotify_audio_analysis_results = get_audio_analysis(item['tracks_ids'], item['tracks_names'], SP)
    fig, ax1 = plt.subplots(figsize=(8,4))
    ax1.plot(spotify_audio_analysis_results.start, spotify_audio_analysis_results.loudness_max, color='r', label='loudness')
    plt.title('Loudness levels of {}'.format(item['tracks_names']))
audio_analysis = {}

for track, item in TRACKS_FOR_AUDIO_ANALYSIS.iterrows():
    audio_analysis[item['tracks_names']] = pd.DataFrame(get_audio_analysis(item['tracks_ids'], item['tracks_names'], SP))
