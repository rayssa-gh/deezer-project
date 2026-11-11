import config
from utils import file_exists, write_csv, read_csv
from data_collector import get_tracks_df, get_genres_df

if __name__ == "__main__":

    # Collecting data

    if file_exists(config.GENRES_CSV):
        df_genres = read_csv(config.GENRES_CSV)
    else:
        df_genres = get_genres_df()
        write_csv(df_genres, config.GENRES_CSV)

    df_tracks = get_tracks_df(df_genres, csv_path=config.TRACKS_CSV)

    # Analysing Data

    print(f"Total tracks in dataset: {len(df_tracks)}")
