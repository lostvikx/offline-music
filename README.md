# Offline Music Downloader

A simple python script to download music from a .csv file.

## Prerequisite

```bash
mkdir ~/Music/docs
```

## Run Script

There are 3 commands that will help you download music offline.

### Download from .csv file

```bash
uv run main.py csv <path_to_music.csv>  # Example: ~/Music/docs/music.csv
```

### Download a YT Playlist

```bash
uv run main.py playlist <playlist_url>
```

### Extract music data from URL (into a .csv)

```bash
uv run main.py extract <url>
```

## Valid CSV File

| Artist      | Song                  |
|-------------|-----------------------|
| Survivor    | Eye of the Tiger      |
| Tom Petty   | Love Is A Long Road   |
