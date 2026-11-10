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
    print(f"Loading from cache: {path}")
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
    print(f"File created and saved: {path}")


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
