import matplotlib.pyplot as plt
import pandas as pd

from get_data import get_spotify
from power import analyze_song_power


def display_power(song_powers, sorted_songs):
    # Visualization of top songs by power score
    plt.figure(figsize=(12, 6))
    powers = [song_powers[song]["power"] for song in sorted_songs[:20]]
    plt.bar(sorted_songs[:20], powers)
    plt.title("Top 20 Songs by Power Score")
    plt.xlabel("Songs")
    plt.ylabel("Power Score")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def display_top_songs():
    df = pd.DataFrame(get_spotify())

    # Analyze song power
    _, sorted_songs, full_df = analyze_song_power(df)

    for song in sorted_songs[:15]:  # Visualize top 5 songs
        visualize_song_plays_over_time(full_df, song)


def visualize_song_plays_over_time(df, song_name, window="1D"):
    """
    Create a time series plot for plays of a specific song

    Parameters:
    - df: DataFrame containing song play data
    - song_name: Name of the song to visualize
    - window: Resampling window (default is daily)
    """
    # Filter for the specific song
    song_df = df[df["master_metadata_track_name"] == song_name].copy()

    # Get the artist name (taking the first one if multiple entries exist)
    artist_name = song_df["master_metadata_album_artist_name"].iloc[0]

    # Set timestamp as index and resample
    song_plays = song_df.set_index("ts").resample(window).size()

    # Create the plot
    plt.figure(figsize=(12, 6))
    ax = song_plays.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title(f"Plays Over Time for '{song_name}' by {artist_name}")
    plt.xlabel("Time")
    plt.ylabel("Number of Plays")

    # Show only every nth label to prevent overcrowding
    n = max(len(ax.get_xticklabels()) // 10, 1)  # Show ~10 labels
    labels = [item.get_text() for item in ax.get_xticklabels()]
    # Convert to just date format (YYYY-MM-DD)
    labels = [label.split(" ")[0] for label in labels]
    ax.set_xticklabels(labels)
    [l.set_visible(False) for (i, l) in enumerate(ax.get_xticklabels()) if i % n != 0]
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = pd.DataFrame(get_spotify())
    # Analyze song power
    song_powers, sorted_songs, _ = analyze_song_power(df)

    display_power(song_powers, sorted_songs)
