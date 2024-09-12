import json
from os import getenv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

root_dir = getenv("EXTENDED_HISTORY_FILES_DIR")


def get_json_data():
    files = [
        "Streaming_History_Audio_2013-2019_0.json",
        "Streaming_History_Audio_2019_1.json",
        "Streaming_History_Audio_2019-2020_2.json",
        "Streaming_History_Audio_2020-2021_3.json",
        "Streaming_History_Audio_2021_4.json",
        "Streaming_History_Audio_2021-2023_5.json",
        "Streaming_History_Audio_2023-2024_6.json",
        # "Streaming_History_Video_2016-2024.json",
    ]

    for json_file in files:
        with open(f"{root_dir}{json_file}") as f:
            json_data = json.load(f)

    return json_data


if __name__ == "__main__":
    df = pd.DataFrame(get_json_data())

    # Convert the 'timestamp' column to datetime
    df["ts"] = pd.to_datetime(df["ts"])

    df["master_metadata_track_name"] = df["master_metadata_track_name"].str.replace(
        "$", "\\$", regex=False
    )

    # Set the time window for resampling (e.g., 30min)
    window = "12H"
    decay_rate = 10

    # Count plays per song
    play_counts = df["master_metadata_track_name"].value_counts()

    # Filter songs with more than 5 plays
    songs_with_enough_plays = play_counts[play_counts > 5].index

    # Filter the DataFrame for these songs
    filtered_df = df[df["master_metadata_track_name"].isin(songs_with_enough_plays)]

    # Function to calculate power with exponential decay
    def calculate_weighted_power(song_df, decay_rate=1.0):
        # Sort by timestamp
        song_df = song_df.sort_values("ts")

        # Compute time differences between consecutive plays
        time_diffs = song_df["ts"].diff().dt.total_seconds().fillna(0)

        # Apply exponential decay (larger time differences get smaller weights)
        weights = np.exp(-time_diffs / decay_rate)

        # Sum the weighted values to get the "power" for the song
        power = weights.sum()
        return power

    # Compute the power for each song
    song_powers = {}
    for song in songs_with_enough_plays:
        song_df = filtered_df[filtered_df["master_metadata_track_name"] == song]
        song_powers[song] = calculate_weighted_power(song_df, decay_rate)

    # Sort songs by power in descending order
    sorted_songs = sorted(song_powers, key=song_powers.get, reverse=True)

    for song in sorted_songs:
        # Filter the DataFrame for the current song
        song_df = filtered_df[filtered_df["master_metadata_track_name"] == song]
        print(song_df["master_metadata_album_artist_name"])

        # Group by song track name and resample by the defined time window, counting plays
        power = (
            song_df.set_index("ts")
            .groupby("master_metadata_track_name")
            .resample(window)
            .size()
        )

        # Fill missing values with zeros for periods where no song was played
        power = power.unstack(fill_value=0).stack()

        # Plot the power of each song over time
        power.unstack("master_metadata_track_name").plot(kind="line", figsize=(10, 6))
        plt.title("Song Power Over Time")
        plt.xlabel("Time")
        plt.ylabel("Play Count (Power)")
        plt.show()
