import os

API_URL = "https://api.deezer.com"
PAUSE = 0.15  # (50 appels / 5 s)
MAX_RETRIES = 5

DATA_DIR = "data"
GENRES_CSV = os.path.join(DATA_DIR, "genres.csv")
TRACKS_CSV = os.path.join(DATA_DIR, "tracks.csv")

GENRE_COLS = ["genre_id", "genre_name"]

EXCLUDE_GENRES = [
    "Livres audio",
    "Jeunesse",
    "Enfants",
    "Films/Jeux vidéo",
    "Bandes originales",
    "Humour",
    "Podcast",
    "Podcasts",
    "Musique du monde",
    "Chanson française",
    "Divers",
    "Inconnu",
    "Musique africaine",
    "Musique arabe",
    "Musique asiatique",
    "Musique brésilienne",
    "Musique indienne",
    "Latino",
]

TRACK_COLS = [
    "track_title",
    "track_duration",
    "track_bpm",
    "track_release_date",
    "track_rank",
    "album_title",
    "album_release_date",
    "label",
    "album_duration",
    "album_nb_fan",
    "record_type",
    "artist_name",
    "nb_album",
    "nb_fan",
    "genre",
]
