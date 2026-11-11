import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

from utils import write_csv

os.makedirs("figures", exist_ok=True)
sns.set_theme(style="whitegrid")


def remove_multi_genre_tracks(csv_path: str = "data/tracks.csv") -> pd.DataFrame:
    """
    Removes tracks belonging to more than 2 genres
    from the CSV file and overwrites it.

    :param csv_path: Path to the CSV file
    :returns: Cleaned DataFrame without multi-genre tracks
    """
    if not os.path.exists(csv_path):
        print(f"File {csv_path} does not exist.\n")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    initial_count = len(df)

    genre_counts = df.groupby("track_title")["genre"].transform("nunique")

    df_clean = df[genre_counts <= 1].copy()

    final_count = len(df_clean)
    removed_count = initial_count - final_count

    write_csv(df_clean, csv_path)

    print(f"Multi-genre filtering complete: {removed_count} rows removed.")
    print(f"Clean dataset saved to {csv_path} ({final_count} rows remaining).\n")

    return df_clean


def plot_general_distributions(df: pd.DataFrame) -> None:
    """
    Generates and saves general distribution plots for track popularity (rank) and duration.

    :param df: The tracks DataFrame
    """
    # Distribution of track_rank
    plt.figure(figsize=(10, 5))
    sns.histplot(df["track_rank"], kde=True, color="royalblue", bins=30)
    plt.title("Distribution de la Popularité des tracks (Rank)")
    plt.xlabel("Rang / Score de popularité")
    plt.ylabel("Nombre de tracks")
    plt.savefig("figures/distribution_popularity.png", bbox_inches="tight")
    plt.close()

    # Distribution of track_duration
    plt.figure(figsize=(10, 5))
    sns.histplot(df["track_duration"], kde=True, color="seagreen", bins=30)
    plt.title("Distribution de la Durée des tracks (Secondes)")
    plt.xlabel("Durée (s)")
    plt.ylabel("Nombre de tracks")
    plt.savefig("figures/distribution_duration.png", bbox_inches="tight")
    plt.close()


def analyze_genre_differences(df: pd.DataFrame) -> dict:
    """
    Generates boxplots for track duration across genres
    and performs ANOVA statistical tests to check if differences are significant.

    :param df: The tracks DataFrame
    :returns: Dictionary containing ANOVA test results (F-statistic and p-value) for track duration
    """
    os.makedirs("figures", exist_ok=True)
    sns.set_theme(style="whitegrid")

    genre_duration_order = (
        df.groupby("genre")["track_duration"].mean().sort_values(ascending=True).index
    )

    # Boxplot: Track duration by genre
    plt.figure(figsize=(14, 7))
    sns.boxplot(
        data=df,
        x="genre",
        y="track_duration",
        order=genre_duration_order,
        palette="Set2",
        hue="genre",
    )
    plt.xticks(rotation=45, ha="right")
    plt.title(
        "Distribution et Comparaison de la Durée des Tracks par Genre (Triés par ordre croissant)"
    )
    plt.xlabel("Genre musical")
    plt.ylabel("Durée (secondes)")
    plt.savefig("figures/boxplot_duration_by_genre.png", bbox_inches="tight")
    plt.close()

    # ANOVA
    duration_groups = [
        group["track_duration"].dropna().values for _, group in df.groupby("genre")
    ]

    f_dur, p_dur = f_oneway(*duration_groups)

    print("--- Résultats du test ANOVA ---")
    print(f"Durée -> F-statistic: {f_dur:.2f} | p-value: {p_dur:.4e}\n")

    return {
        "duration_anova": {"f_stat": f_dur, "p_value": p_dur},
    }


def plot_popularity_vs_fans(df: pd.DataFrame) -> None:
    """
    Generates a Spearman correlation heatmap to analyze the relationship
    between numerical variables such as track popularity, fans, and album metrics.

    :param df: The tracks DataFrame
    :returns: None
    """
    os.makedirs("figures", exist_ok=True)

    # Heatmap
    plt.figure(figsize=(8, 6))
    numeric_cols = [
        "track_rank",
        "album_nb_fan",
        "nb_fan",
        "nb_album",
    ]
    corr_matrix = df[numeric_cols].corr(method="spearman")

    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
    plt.title("Matrice de Corrélation de Spearman")
    plt.savefig("figures/correlation_heatmap.png", bbox_inches="tight")
    plt.close()


def plot_genre_release_year(df: pd.DataFrame) -> None:
    """
    Generates a stacked bar chart showing the proportion of
    release year bin for each musical genre.

    :param df: The tracks DataFrame
    :returns: None
    """
    os.makedirs("figures", exist_ok=True)
    sns.set_theme(style="whitegrid")

    data = df.copy()
    data["release_year"] = pd.to_datetime(
        data["track_release_date"], errors="coerce"
    ).dt.year
    data = data.dropna(subset=["release_year", "genre"])

    # Year bins
    bins = [0, 1999, 2010, 2020, 2026]
    labels = ["Avant 2000", "2000-2010", "2011-2020", "2021-2026"]
    data["year_bin"] = pd.cut(data["release_year"], bins=bins, labels=labels)

    cross_tab = pd.crosstab(data["genre"], data["year_bin"], normalize="index") * 100

    if "2021-2026" in cross_tab.columns:
        cross_tab = cross_tab.sort_values(by="2021-2026", ascending=False)

    fig, ax = plt.subplots(figsize=(14, 8))

    colors = [
        "#d9d9d9",
        "#9ecae1",
        "#41b6c4",
        "#225ea8",
    ]

    cross_tab.plot(
        kind="bar", stacked=True, ax=ax, color=colors, edgecolor="white", width=0.8
    )

    plt.title("Répartition des Tranches d'Années par Genre Musical (Proportion 100%)")
    plt.xlabel("Genre musical")
    plt.ylabel("Pourcentage (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Tranches d'années", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    plt.savefig("figures/genre_release_year_stacked_bar.png", bbox_inches="tight")
    plt.close()
