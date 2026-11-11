import os
import pandas as pd
import time
import requests
import config


def file_exists(path: str) -> bool:
    """
    Checks if a given file exists.

    :param path: Path to the file
    :returns: True if the file exists, False otherwise
    """
    return os.path.isfile(path)


def read_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.

    :param path: Path to the CSV file
    :returns: pd.DataFrame containing the file data
    """
    print(f"Loading from cache: {path}\n")
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    Writes a DataFrame to a CSV file, creating parent directories if needed.

    :param df: DataFrame to write
    :param path: Destination path for the CSV file
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    df.to_csv(path, index=False)
    print(f"File created and saved: {path}\n")


def get(path, **params):
    """
    Performs a GET request to the Deezer API.

    :param path: API endpoint path
    :param params: Optional query parameters
    :returns: JSON response dict, or None if an error occurs
    """
    for _ in range(config.MAX_RETRIES):
        time.sleep(config.PAUSE)
        try:
            data = requests.get(
                f"{config.API_URL}/{path}", params=params, timeout=15
            ).json()
        except (requests.RequestException, ValueError):
            time.sleep(2)
            continue

        error = data.get("error") if isinstance(data, dict) else None
        if error is None:
            return data
        if error.get["code"] == 4:
            time.sleep(5)
            continue
        print(f"API Error on {path} : {error}")
        return None
    return None


def get_data(path, **params):
    """
    Calls get() and extracts the 'data' list from the response.

    :param path: API endpoint path
    :param params: Optional query parameters
    :returns: List of items, or empty list
    """
    data_json = get(path, **params) or {}
    return data_json.get("data", [])


def load_cache(csv_path: str) -> tuple[set, dict]:
    """
    Loads an existing CSV file to create a cache of already downloaded tracks.

    :param csv_path: Path to the CSV file
    :returns: A tuple with the set of seen (track, genre) pairs and the tracks dictionary cache
    """
    seen_pairs = set()
    track_cache = {}

    if not os.path.exists(csv_path):
        return seen_pairs, track_cache

    print(f"Loading existing data from {csv_path} for caching...\n")
    df_existing = pd.read_csv(csv_path)

    if df_existing.empty or "track_id" not in df_existing.columns:
        return seen_pairs, track_cache

    seen_pairs = set(zip(df_existing["track_id"], df_existing["genre"]))

    for _, row in df_existing.iterrows():
        t_id = row["track_id"]
        if t_id not in track_cache:
            track_cache[t_id] = row.to_dict()

    print(f"Cache loaded: {len(seen_pairs)} unique (track, genre) pairs found.")
    print(f"Track details cache: {len(track_cache)} unique tracks found.\n")

    return seen_pairs, track_cache
