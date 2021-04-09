# Overview

In this repo we have 3 packages: get_data_from_spotify, audio_analysis_to_dash y audio_analysis_to_streamlit. The reason to have this 3 packages together in this same repository in the inner project nature. which divides the steps (in a wide view) like this:

* Get Ids from a significative sample of songs (6.000) through Spotify API.
* Through this Ids, get the [audio analysis of this songs](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-analysis)
* Generate a csv.
* Test infrastructure tools for dashboarding Dash & Streamlit to visualize data from the songs.

I develop this using windows, so if you're using linux or os, I write some notes at the end to guide in the syntax process.

* [Usage](#Usage)
  * [install](#installation)
  * [unittest discovery](#unit-tests)
  * [flake8 linting](#flake8-linting)
  * [mypy type checks](#mypy-type-checks)
  * [folders](#folders)
  * [linux and os specs](#linux-and-os)
* [Dash](#dash)
* [Streamlit](#streamlit)

## Usage
We assume credentials are kept in the `credentials/` directory on a json format (client_id: XXXX...), which is .gitignored.

Needed credentials:
* `credentials/spotify_credentials.json`:[to get credentials for spotify API](https://developer.spotify.com/documentation/web-api/quick-start/)

Through this commands we can call each step of the workflow (full workflow script is coming):

* Get Tracks data & ids:
```bash
env\Scripts\python -m audio_analysis_to_dash.get_tracks^
  --directory test_dir^
  --credentials_path credentials\spotify_credentials.json
```
* Get audio analysis from ids:
```bash
env\Scripts\python -m audio_analysis_to_dash.get_audio_analysis^
  --directory audio_analysis^
  --tracks_path test_dir\tracks.json^
  --spotify_credentials_path credentials\spotify_credentials.json
```
* Generate a csv with all the information:
```bash
env\Scripts\python -m audio_analysis_to_dash.join_data^
    --directory_tracks test_dir^
    --directory_audio audio_analysis^
    --filename results\joined_data.csv
```
### installation

  1. install virtualenv:
    `python -m venv env`
  2. install requirements in virtual env:
    `env\Scripts\pip install -r requirements.txt`
  3. you can launch an interpreter in the env context like this:
    `env\Scripts\python`
  4. check your creds are correct:
    `env\Scripts\python -m get_data_from_spotify.get_tracks`

#### unit tests
To run unit tests using the built-in [test discovery mechanism](https://docs.python.org/3/library/unittest.html#unittest-test-discovery), simply run:

```bash
env\Scripts\python -m unittest discover
```

#### flake8 linting

Run flake8 on the packages:
```
env\Scripts\python -m flake8 --select F audio_analysis_to_dash
```  
```
env\Scripts\python -m flake8 --select F audio_analysis_to_streamlit
```  
and
```
env\Scripts\python -m flake8 --select F get_data_from_spotify
```

#### mypy type checks

This runs [mypy](http://mypy-lang.org/) static typechecks on the code:
```
env\Scripts\python -m mypy --check-untyped-defs --ignore-missing-imports audio_analysis_to_dash
```
```
env\Scripts\python -m mypy --check-untyped-defs --ignore-missing-imports audio_analysis_to_streamlit
```  
and
```
env\Scripts\python -m mypy --check-untyped-defs --ignore-missing-imports get_data_from_spotify
```
#### folders
For this to run correctly we need 2 folders:
* **test_dir**
* **audio_analysis**

#### mac and os
You need to change syntax of the calls like this:

* env\Scripts\python -> env/bin/python
* The ^ as line break -> \

## Dash
This allows you to launch the dashboard on dash on a local server:
```
env\Scripts\python -m audio_analysis_to_dash.data_to_dash
```
To put this dashboard on a server, we can use a tool like [Heroku](https://www.heroku.com/)

## Streamlit

This allows you to launch the dashboard on streamlit on a local server:
```
env\Scripts\streamlit run audio_analysis_to_streamlit\data_to_streamlit.py
```
To share publicly this dashboard, you have to [ask for a invitation](https://streamlit.io/sharing)
