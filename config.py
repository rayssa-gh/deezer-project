import os

API_URL = "https://api.deezer.com"
PAUSE = 0.15  # (50 appels / 5 s)
MAX_RETRIES = 5

DATA_DIR = "data"
GENRES_CSV = os.path.join(DATA_DIR, "genres.csv")


GENRE_COLS = ["genre_id", "genre_name"]
ARTIST_COLS = ["artist_id", "artist_name", "nb_album", "nb_fan"]
ALBUM_COLS = [
    "album_id",
    "album_title",
    "album_release_date",
    "label",
    "album_duration",
    "album_nb_fan",
    "record_type",
    "album_artist_id",
]
TRACK_COLS = [
    "track_id",
    "track_title",
    "track_duration",
    "track_bpm",
    "track_release_date",
    "track_rank",
    "album_id",
    "artist_id",
    "sampled_genre_id",
]
