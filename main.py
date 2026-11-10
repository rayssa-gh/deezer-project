import pandas as pd
import config
from utils import file_exists, write_csv, read_csv, get_data


def get_genres_df() -> pd.DataFrame:
    """
    Fetches genres from the Deezer API and builds a DataFrame.

    :returns: pd.DataFrame with genre_id and genre_name
    """
    print("Fetching genres from Deezer API...")
    rows = [
        {"genre_id": g["id"], "genre_name": g["name"]}
        for g in get_data("genre")
        if g["id"] != 0
    ]
    return pd.DataFrame(rows, columns=config.GENRE_COLS).sort_values(
        by="genre_id", ascending=True
    )


if __name__ == "__main__":

    if file_exists(config.GENRES_CSV):
        df_genres = read_csv(config.GENRES_CSV)
    else:
        df_genres = get_genres_df()
        write_csv(df_genres, config.GENRES_CSV)

    print(df_genres.head())

    # if file_exists(config.ARTISTS_CSV):
    #     df_artists = read_csv(config.ARTISTS_CSV)
    # else:
    #     df_artists = get_artists_df()
    #     write_csv(df_artists, config.ARTISTS_CSV)
