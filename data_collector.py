import os
import pandas as pd
import config
from utils import (
    get_data,
    get,
    write_csv,
    load_cache,
)


def get_genres_df() -> pd.DataFrame:
    """
    Gets music genres from the Deezer API, removes non-musical ones, and builds a table.

    :returns: DataFrame with valid genre IDs and names
    """
    print("Fetching and filtering genres from Deezer API...")
    rows = [
        {"genre_id": g["id"], "genre_name": g["name"]}
        for g in get_data("genre")
        if g["id"] != 0 and g["name"] not in config.EXCLUDE_GENRES
    ]

    return (
        pd.DataFrame(rows, columns=config.GENRE_COLS)
        .sort_values(by="genre_id", ascending=True)
        .reset_index(drop=True)
    )


def get_tracks_df(
    genres_df: pd.DataFrame, csv_path: str = "tracks.csv"
) -> pd.DataFrame:
    """
    Gets top tracks from each genre chart, uses cache to avoid duplicates,
    and saves data to CSV after each genre.

    :param genres_df: DataFrame with filtered genres
    :param csv_path: Path to the CSV file where data is saved
    :returns: DataFrame with all collected tracks
    """

    seen_track_genre_pairs, track_cache = load_cache(csv_path)

    for _, genre_row in genres_df.iterrows():
        genre_id = genre_row["genre_id"]
        genre_name = genre_row["genre_name"]
        print(f"\n--- Processing genre: {genre_name} (ID: {genre_id}) ---")

        chart_tracks_data = get_data(f"chart/{genre_id}/tracks", limit=100)
        genre_rows = []

        for track in chart_tracks_data:
            track_id = track.get("id")

            if not track_id:
                continue

            pair = (track_id, genre_name)

            print(pair)

            if pair in seen_track_genre_pairs:
                continue

            if track_id in track_cache:
                track_record = track_cache[track_id].copy()
                track_record["genre"] = genre_name
            else:
                album_id = (track.get("album") or {}).get("id")
                album_details = get(f"album/{album_id}") or {} if album_id else {}

                artist_id = (track.get("artist") or {}).get("id")
                artist_details = get(f"artist/{artist_id}") or {} if artist_id else {}

                track_record = build_chart_track_record(
                    track=track,
                    album_details=album_details,
                    artist_details=artist_details,
                    genre_name=genre_name,
                )
                track_cache[track_id] = track_record

            seen_track_genre_pairs.add(pair)
            genre_rows.append(track_record)

        if genre_rows:
            df_genre_new = pd.DataFrame(genre_rows, columns=config.TRACK_COLS)

            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
                df_combined = pd.concat([df_existing, df_genre_new])
            else:
                df_combined = df_genre_new

            write_csv(df_combined, csv_path)
            print(
                f"{len(genre_rows)} new rows added for '{genre_name}' (Total in CSV: {len(df_combined)})"
            )

    return (
        pd.read_csv(csv_path)
        if os.path.exists(csv_path)
        else pd.DataFrame(columns=config.TRACK_COLS)
    )


def build_chart_track_record(
    track: dict, album_details: dict, artist_details: dict, genre_name: str
) -> dict:
    """
    Creates a clean dictionary for a track with zero None values using track, album, and artist data.

    :param track: Raw track data dictionary from API
    :param album_details: Detailed album data dictionary from API
    :param artist_details: Detailed artist data dictionary from API
    :param genre_name: Name of the music genre
    :returns: Cleaned dictionary with all track details
    """

    return {
        "track_id": track.get("id") or 0,
        "track_title": track.get("title") or "Inconnu",
        "track_duration": track.get("duration") or 0,
        "track_bpm": track.get("bpm") or 0,
        "track_release_date": track.get("release_date")
        or album_details.get("release_date")
        or None,
        "track_rank": track.get("rank") or 0,
        "album_title": album_details.get("title") or {} or "Inconnu",
        "album_release_date": album_details.get("release_date")
        or track.get("release_date")
        or None,
        "label": album_details.get("label") or "Indépendant / Inconnu",
        "album_duration": album_details.get("duration") or 0,
        "album_nb_fan": album_details.get("fans") or 0,
        "record_type": album_details.get("record_type") or "album",
        "artist_name": artist_details.get("name") or "Inconnu",
        "nb_album": artist_details.get("nb_album") or 0,
        "nb_fan": artist_details.get("nb_fan") or 0,
        "genre": genre_name,
    }
