# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "lxml",
#     "numpy",
#     "pandas",
#     "requests",
# ]
# ///

import os
import sys
import subprocess
import random
import requests
import time

import numpy as np
import pandas as pd

from urllib.parse import urlencode

# TODO []: Error handling.
# TODO [*]: Download songs from a .csv file.
# TODO [*]: Download a YouTube playlists.
# TODO [*]: Download tables from a URL to a .csv file.
# TODO [*]: Prompt a destination directory.

def fetch_yt_music_url(search_query):
    print(f'Fetching URL For: {search_query}')

    params = { "q": search_query }
    encoded_query = urlencode(params)

    url = "https://music.youtube.com/youtubei/v1/search"

    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "cookie": "YSC=okMk8BqCLnU; VISITOR_INFO1_LIVE=9T7zfk_nv2E; VISITOR_PRIVACY_METADATA=CgJJThIEGgAgFA%3D%3D",
        "dnt": "1",
        "origin": "https://music.youtube.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://music.youtube.com/search?{encoded_query}",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version-list": '"Brave";v="131.0.0.0", "Chromium";v="131.0.0.0", "Not_A Brand";v="24.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.9.3"',
        "sec-ch-ua-wow64": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "same-origin",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-goog-visitor-id": "Cgs5VDd6ZmtfbnYyRSjLsKq7BjIKCgJJThIEGgAgFA%3D%3D",
        "x-youtube-bootstrap-logged-in": "false",
        "x-youtube-client-name": "67",
        "x-youtube-client-version": "1.20241218.01.00",
    }

    # Data (raw JSON payload)
    data = {
        "context": {
            "client": {
                "hl": "en",
                "gl": "IN",
                "remoteHost": "2405:201:1d:7843:2047:8fb8:5378:f634",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "Cgs5VDd6ZmtfbnYyRSjLsKq7BjIKCgJJThIEGgAgFA%3D%3D",
                "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36,gzip(gfe)",
                "clientName": "WEB_REMIX",
                "clientVersion": "1.20241218.01.00",
                "osName": "X11",
                "osVersion": "",
                "originalUrl": f"https://music.youtube.com/search?{encoded_query}",
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "configInfo": {
                    "appInstallData": "CMuwqrsGELekzhwQt--vBRCB1rEFEOCN_xIQvbauBRCSy7EFENPhrwUQt-r-EhDTuc4cENmqzhwQ37TOHBDnms4cEOK4sAUQ65mxBRDBq84cEMO7zhwQg8OxBRCVsc4cEIjjrwUQgcOxBRDJ968FEI_DsQUQj8LOHBD_3v8SEMTYsQUQytSxBRCvwc4cEOilzhwQzN-uBRCM0LEFEL2KsAUQ7bmxBRD4q7EFEJuqsQUQwrfOHBDevM4cEJrOsQUQj63OHBDx3v8SEOW5sQUQ0I2wBRCtns4cEIqhsQUQjtCxBRDBzbEFEIfDsQUQhaexBRDnqM4cEL2ZsAUQ5s-xBRCKrs4cEPyyzhwQqabOHBCL1LEFELuszhwQ6sOvBRCZjbEFEJT-sAUQppOxBRDerbEFEParsAUQytixBRDJ5rAFEJmYsQUQmdL_EhDI2LEFEMC3zhwQ8ZywBRDr6P4SEKuezhwQjtexBRCe0LAFEKKjzhwQsJ3OHBDW4_8SEPq4zhwQiIewBRCi1LEFEI3UsQUQ0ZTOHBCUu84cEMbYsQUQqJqwBRD0s84cEJi7zhwQ98HOHCocQ0FNU0R4VU1vTDJ3RE5Ia0J1SGRoUW9kQnc9PQ%3D%3D",
                },
            },
            "user": {"lockedSafetyMode": False},
            "request": {"useSsl": True, "internalExperimentFlags": [], "consistencyTokenJars": []},
            "adSignalsInfo": {
                "params": [
                    {"key": "dt", "value": "1735039052514"},
                    {"key": "flash", "value": "0"},
                    {"key": "frm", "value": "0"},
                    {"key": "u_tz", "value": "330"},
                ]
            },
        },
        "query": search_query,
        "suggestStats": {
            "validationStatus": "VALID",
            "parameterValidationStatus": "VALID_PARAMETERS",
            "clientName": "youtube-music",
        },
    }

    # Make the POST request
    response = requests.post(url, json=data, headers=headers)

    # Check the response
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")

    try:
        music_id = response.json()['contents']['tabbedSearchResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][1]['musicShelfRenderer']['contents'][0]['musicResponsiveListItemRenderer']['overlay']['musicItemThumbnailOverlayRenderer']['content']['musicPlayButtonRenderer']['playNavigationEndpoint']['watchEndpoint']['videoId']
    except KeyError as error:
        print('Could not find the song URL.')
        return np.nan
    
    song_url = f'https://music.youtube.com/watch?v={music_id}'
    return song_url


def download_song(song_url, dir_name):
    music_dir_path = os.path.join('~/Music', dir_name, f"%(title)s.%(ext)s")
    command = ["yt-dlp", "--config-locations", "~/.config/yt-dlp/music-config.conf", song_url, "-o", music_dir_path]
    subprocess.run(command)


def fetch_urls(row):
    try:
        search_query = f"{row.loc['Artist']} - {row.loc['Song']}"
    except KeyError:
        search_query = f"{row.iloc[0]} - {row.iloc[1]}"
    except Exception as error:
        exit(f'Something went wrong: {error}')

    yt_music_url = fetch_yt_music_url(search_query)

    time.sleep(10 + random.randint(1, 10))
    return yt_music_url


def download_from_csv(csv_file):
    try:
        music_library = pd.read_csv(csv_file)
    except Exception as error:
        exit(f'Error in parsing csv file: {error}')
    
    print(f"Please verify your table:\n\n{music_library.head(3)}\n")

    # ans = input('Do you wish to continue with the download? [y/N] ').strip()
    # if ans.lower() != 'y':
    #     exit('Abort.')

    if 'URL' not in music_library.columns:
        music_library['URL'] = np.nan

    music_library['URL'] = music_library.apply(lambda row: fetch_urls(row) if pd.isna(row['URL']) else row['URL'], axis=1) 
    music_library.to_csv(csv_file, index=False)

    dir_name = input('Enter directory name: ').strip() or ''
    dir_path = os.path.join('/', 'home', 'vik', 'Music', dir_name)
    os.path.exists(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for (i, row) in music_library.iterrows():

        song_url = row.loc['URL']

        if pd.isna(song_url):
            print(f'Download Canceled: {row.iloc[0]} - {row.iloc[1]}')
            continue
        
        print(f'Downloading: {row.iloc[0]} - {row.iloc[1]}')
        download_song(song_url, dir_name)
        time.sleep(10 + random.randint(1, 10))


def download_from_playlist(playlist_url):
    command = ['yt-dlp', "--config-locations", "~/.config/yt-dlp/music-config.conf", playlist_url]
    subprocess.run(command)


def extract_table(url):
    """Extract tables from website: vgost.fandom.com"""
    try:
        tables = pd.read_html(url)
    except Exception as error:
        exit(f'Error in reading table in HTML: {error}')
    
    if len(tables) > 1:
        print('Ignoring the last table.')
        tables = tables[:-1]

    df = pd.concat(tables).reset_index(drop=True)
    df = df.iloc[:, :-1]
    df = df.drop_duplicates(df.columns[1])
    df = df.dropna(axis=0)

    file_name = input('Enter file name: ').strip()
    df.to_csv(f'{file_name}.csv', index=False)

    ans = input('Do you wish to download the music? [y/N] ').strip()
    if ans.lower() != 'y':
        exit('Abort.')

    download_from_csv(f'{file_name}.csv')


def main():
    if len(sys.argv) != 3:
        exit('Not enough arguments provided.\nSyntax: python main.py [csv|playlist|extract] <argument>')

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == 'csv':
        download_from_csv(arg)
    elif command == 'playlist':
        download_from_playlist(arg)
    elif command == 'extract':
        extract_table(arg)
    else:
        exit('Invalid command.\nValid commands: [csv|playlist|extract].')
    
    print('---'*10)
    print('Download Complete.')


if __name__ == "__main__":
    main()
