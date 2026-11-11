import config
from utils import file_exists, write_csv, read_csv
from data_collector import get_tracks_df, get_genres_df
from data_analyser import (
    remove_multi_genre_tracks,
    analyze_genre_differences,
    plot_general_distributions,
    plot_popularity_vs_fans,
    plot_genre_release_year,
)

if __name__ == "__main__":

    # Partie 1: Collecte de données

    if file_exists(config.GENRES_CSV):
        df_genres = read_csv(config.GENRES_CSV)
    else:
        df_genres = get_genres_df()
        write_csv(df_genres, config.GENRES_CSV)

    df_tracks = get_tracks_df(df_genres, csv_path=config.TRACKS_CSV)

    # Partie 2: Analyse de données

    print(f"Total tracks in dataset: {len(df_tracks)}\n")

    df_tracks = remove_multi_genre_tracks(config.TRACKS_CSV)
    plot_general_distributions(df_tracks)

    # q1: corrélation entre rank et fans
    plot_popularity_vs_fans(df_tracks)

    # q2: durée par genre
    analyze_genre_differences(df_tracks)

    # q3: années les plus representées par genre
    plot_genre_release_year(df_tracks)
