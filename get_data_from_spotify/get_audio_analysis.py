import spotipy
import argparse
import json
import os
from typing import Dict, List, Any
from spotipy.oauth2 import SpotifyClientCredentials
from get_data_from_spotify import get_tracks


def track_analysis_to_directory(directory: str, data: Any, filename: Any) -> None:
    #writing email data to files in directory
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        return json.dump(data, f)

def make_track_analysis(track_id:str, time:str, loudness:str) -> Dict:
    return {
        'track_id': track_id,
        'time': time,
        'loudness': loudness
    }

def get_audio_analysis(track_id:str, spotify_api:Any) -> List:
    audio_analysis = []
    data = spotify_api.audio_analysis(track_id)
    for i in data['segments']:
        tracks_audio = make_track_analysis(
                track_id = track_id,
                time = i['start'],
                loudness = i['loudness_max'])
        audio_analysis.append(tracks_audio)
    return(audio_analysis)

def dump(directory: str, tracks_path: str, spotify_credentials_path: str) -> None:
    #dumping all email data indivudally to file
    credentials = get_tracks.load_json(spotify_credentials_path)
    SP = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=credentials['client_id'], client_secret=credentials['client_secret']))
    tracks = get_tracks.load_json(tracks_path)
    for track in tracks:
        audio_analysis = get_audio_analysis(track['track_id'], SP)
        if audio_analysis != None:
            track_analysis_to_directory(directory, audio_analysis, "{}.json".format(track['track_id']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a file per track in a directory"
    )

    parser.add_argument(
        "--directory",
        required=True,
        type=str,
        help="path to directory to write the files")

    parser.add_argument(
        "--tracks_path",
        required=True,
        type=str,
        help="path to directory where to extract tracks ids")

    parser.add_argument(
        "--spotify_credentials_path",
        required=True,
        type=str,
        help="path to credentials")

    args = parser.parse_args()

    dump(args.directory, args.tracks_path, args.spotify_credentials_path)
