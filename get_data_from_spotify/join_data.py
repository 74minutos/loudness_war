import json
import argparse
import os
import pandas as pd
from typing import Any

def getting_data_to_join(directory_path: str) -> Any:
    directory_files = os.listdir(directory_path)
    for file in directory_files:
        if file.endswith(".json"):
            json_path = os.path.join(directory_path, file)
            with open(json_path) as read_from_directory:
                data =  json.load(read_from_directory)
                yield (data)

def data_to_csv(directory_tracks: str, directory_audio: str, filename:str):
    tracks = []
    audios = []
    for tracks_data in getting_data_to_join(directory_tracks):
        for track in tracks_data:
            tracks.append(track)
    for audio_data in getting_data_to_join(directory_audio):
        for audio in audio_data:
            audios.append(audio)
    tracks_data = pd.DataFrame(tracks)
    audio_data = pd.DataFrame(audios)
    joining_data = tracks_data.merge(audio_data, on='track_id', how='inner')
    #csv to directory
    joining_data.to_csv(filename, sep=';', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Load track and audio data and create an output join file."
    )

    parser.add_argument(
        "--directory_tracks",
        required=True,
        type=str,
        help="path to directory to load email data")

    parser.add_argument(
        "--directory_audio",
        required=True,
        type=str,
        help="path to directory to load events data")

    parser.add_argument(
        "--filename",
        required=True,
        type=str,
        help="name for csv file")

    args = parser.parse_args()

    data_to_csv(args.directory_tracks, args.directory_audio, args.filename)




#for track, item in TRACKS_FOR_AUDIO_ANALYSIS.iterrows():
    #spotify_audio_analysis_results = get_audio_analysis(item['tracks_ids'], item['tracks_names'], SP)
    #fig, ax1 = plt.subplots(figsize=(8,4))
    #ax1.plot(spotify_audio_analysis_results.start, spotify_audio_analysis_results.loudness_max, color='r', label='loudness')
    #plt.title('Loudness levels of {}'.format(item['tracks_names']))
