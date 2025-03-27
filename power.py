from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from get_data import get_spotify


def calculate_weighted_power(song_df, decay_rate=300):
    # Sort by timestamp
    song_df = song_df.sort_values("ts")

    # Calculate the total time span of the song's plays
    time_span = (song_df["ts"].max() - song_df["ts"].min()).total_seconds()

    # Compute time differences between consecutive plays
    time_diffs = song_df["ts"].diff().dt.total_seconds().fillna(0)

    # Apply exponential decay (larger time differences get smaller weights)
    weights = np.exp(-time_diffs / decay_rate)

    # Penalize songs with very long time spans between first and last play
    # But not completely - allow for rediscovery of old songs
    span_penalty = 1 / (1 + np.log(time_span / (30 * 24 * 3600) + 1))

    # Sum the weighted values to get the "power" for the song
    power = weights.sum() * span_penalty

    return power


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


def analyze_song_power(df, decay_rate=300, min_plays=5):
    # Convert the 'timestamp' column to datetime
    df["ts"] = pd.to_datetime(df["ts"])

    # Escape special characters in track names
    df["master_metadata_track_name"] = df["master_metadata_track_name"].str.replace(
        "$", "\\$", regex=False
    )

    # Count plays per song
    play_counts = df["master_metadata_track_name"].value_counts()

    # Filter songs with more than min_plays
    songs_with_enough_plays = play_counts[play_counts > min_plays].index

    # Filter the DataFrame for these songs
    filtered_df = df[df["master_metadata_track_name"].isin(songs_with_enough_plays)]

    # Compute the power for each song
    song_powers = {}
    for song in songs_with_enough_plays:
        song_df = filtered_df[filtered_df["master_metadata_track_name"] == song]
        song_powers[song] = {
            "power": calculate_weighted_power(song_df, decay_rate),
            "artist": song_df["master_metadata_album_artist_name"].iloc[0],
            "total_plays": len(song_df),
            "first_play": song_df["ts"].min(),
            "last_play": song_df["ts"].max(),
        }

    # Sort songs by power in descending order
    sorted_songs = sorted(
        song_powers, key=lambda x: song_powers[x]["power"], reverse=True
    )

    # Print out detailed results
    print("Top Songs by Power Analysis:")
    for song in sorted_songs[:10]:  # Top 10 songs
        details = song_powers[song]
        print(f"Song: {song}")
        print(f"Artist: {details['artist']}")
        print(f"Power Score: {details['power']:.2f}")
        print(f"Total Plays: {details['total_plays']}")
        print(f"First Played: {details['first_play']}")
        print(f"Last Played: {details['last_play']}")
        print("---")

    return song_powers, sorted_songs, df


if __name__ == "__main__":
    # Load the data
    df = pd.DataFrame(get_spotify())

    # Analyze song power
    song_powers, sorted_songs, full_df = analyze_song_power(df)

    # # Visualization of top songs by power score
    # plt.figure(figsize=(12, 6))
    # powers = [song_powers[song]["power"] for song in sorted_songs[:20]]
    # plt.bar(sorted_songs[:20], powers)
    # plt.title("Top 20 Songs by Power Score")
    # plt.xlabel("Songs")
    # plt.ylabel("Power Score")
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.show()

    # Optional: Visualize plays over time for top songs
    for song in sorted_songs[:15]:  # Visualize top 5 songs
        visualize_song_plays_over_time(full_df, song)
