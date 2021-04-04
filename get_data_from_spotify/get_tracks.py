import spotipy
import argparse
import json
import os
from typing import Dict, List, Any
from spotipy.oauth2 import SpotifyClientCredentials

def load_json(file_path: str) -> Dict:
    with open(file_path) as read_from_file:
        data = json.load(read_from_file)
        return data

DECADES = ['year:1960-1969',
    'year:1970-1979',
    'year:1980-1989',
    'year:1990-1999',
    'year:2000-2009',
    'year:2010-2019',
    'year:2020-2029']

def make_track(track_name:str, track_id:str, album_name:str, artist_name:str, popularity:str, decade:str) -> Dict:
    return {
        'track_name': track_name,
        'track_id': track_id,
        'album_name': album_name,
        'artist_name': artist_name,
        'popularity': popularity,
        'decade': decade
    }
TRACKS = []

def get_first_year_from_decade(decade:str) -> str:
    span = decade.split(':')[1]
    first_year, last_year = span.split('-')
    return first_year


def get_tracks(decade: str, spotify_api:Any) -> List:
    tracks = []
    year = get_first_year_from_decade(decade)
    for i in range(0,1000, 50):
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
    TRACKS.extend(tracks)
    return TRACKS

def tracks_to_file(directory: str, data: Any) -> None:
    #creating the file with email ids
    filename = "tracks.json"
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        return json.dump(data, f)

def dump(directory: str, credentials_path: str) -> None:
    credentials = load_json(credentials_path)
    SP = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=credentials['client_id'], client_secret=credentials['client_secret']))
    for decade in DECADES:
        track = get_tracks(decade, SP)
        tracks_to_file(directory, track)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create a file with all tracks."
    )

    parser.add_argument(
        "--directory",
        required=True,
        type=str,
        help="path to directory to write the files")

    parser.add_argument(
        "--credentials_path",
        required=True,
        type=str,
        help="path to credentials")

    args = parser.parse_args()

    dump(args.directory, args.credentials_path)
