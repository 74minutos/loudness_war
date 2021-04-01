





env\Scripts\python -m audio_analysis_to_dash.get_tracks^
  --directory test_dir^
  --credentials_path credentials\spotify_credentials.json

env\Scripts\python -m audio_analysis_to_dash.get_audio_analysis^
  --directory audio_analysis^
  --tracks_path test_dir\tracks.json^
  --spotify_credentials_path credentials\spotify_credentials.json

env\Scripts\python -m audio_analysis_to_dash.join_data^
    --directory_tracks test_dir^
    --directory_audio audio_analysis^
    --filename results\joined_data.csv
