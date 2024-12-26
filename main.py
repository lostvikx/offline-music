# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy",
#     "pandas",
#     "requests",
# ]
# ///

import sys
import subprocess
import requests
import time

import numpy as np
import pandas as pd

from urllib.parse import urlencode

# TODO: Error handling.


def fetch_yt_music_url(search_query):
    print(f'Fetching URL: {search_query}')

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

    music_id = response.json()['contents']['tabbedSearchResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][1]['musicShelfRenderer']['contents'][1]['musicResponsiveListItemRenderer']['playlistItemData']['videoId']
    
    song_url = f'https://music.youtube.com/watch?v={music_id}'
    return song_url


def download_song(song_url):
    command = ['yt-dlp', "--config-locations", "~/.config/yt-dlp/music-config.conf", song_url]
    subprocess.run(command)


def main():
    if len(sys.argv) != 2:
        exit('Please add the argument.')

    csv_file = sys.argv[1]
    music_library = pd.read_csv(csv_file)

    def fetch_urls(row):
        try:
            search_query = f"{row.loc['Artist']} - {row.loc['Song']}"
        except KeyError:
            search_query = f"{row.iloc[0]} - {row.iloc[1]}"
        except Exception as error:
            exit(f'Something went wrong: {error}')

        time.sleep(10)

        return fetch_yt_music_url(search_query)

    if 'URL' not in music_library.columns:
        music_library['URL'] = np.nan

    music_library['URL'] = music_library.apply(lambda row: fetch_urls(row) if pd.isna(row['URL']) else row['URL'], axis=1) 
    music_library.to_csv(csv_file, index=False)

    print(music_library.head())


if __name__ == "__main__":
    main()
