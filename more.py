import pandas as pd


def sort_artists():
    total_time = 0
    song_plays: dict[str, int] = {}
    artists: dict[str, int] = {}

    for song in get_spotify():
        ms = song.get("ms_played")
        total_time += ms

        title = song.get("master_metadata_track_name")
        artist = song.get("master_metadata_album_artist_name")
        if f"{title}\t {artist}" not in song_plays.keys():
            song_plays[f"{title}\t {artist}"] = 1
        else:
            song_plays[f"{title}\t {artist}"] += 1
        if not artist:
            artist = song.get("episode_show_name")
        if artist == None:
            song.pop("ts")
            song.pop("username")
            song.pop("platform")
            song.pop("ms_played")
            song.pop("conn_country")
            song.pop("ip_addr_decrypted")
            song.pop("user_agent_decrypted")
            song.pop("reason_start")
            song.pop("reason_end")
            song.pop("shuffle")
            song.pop("skipped")
            song.pop("offline")
            song.pop("offline_timestamp")
            song.pop("incognito_mode")
            for item in song:
                if song[item] != None:
                    print(f"{item}: {song[item]}")
        if artist not in artists.keys():
            artists[artist] = ms
        artists[artist] += ms

    hours = int(total_time * (2.7 * 10**-7))
    days = int(hours / 24)
    print(f"hours: {hours}")
    print(f"days: {days}")

    sorted_artists = dict(sorted(artists.items(), key=lambda item: item[1]))

    sorted_titles = dict(sorted(song_plays.items(), key=lambda item: item[1]))

    # print(sorted_titles)
    print(sorted_artists)


def calculate_power_score(row):
    ms_played = row["ms_played"]
    skipped = row["skipped"]
    total_duration = row["duration_ms"]

    seconds_played = ms_played / 1000
    total_seconds = total_duration / 1000
    base_score = 100

    if skipped:
        percentage_played = seconds_played / total_seconds
        if percentage_played < 0.1:
            return 10
        elif percentage_played < 0.5:
            return int(base_score * percentage_played)
        else:
            return int(base_score * (0.5 + percentage_played / 2))
    else:
        return base_score + min(int(total_seconds / 60), 20)


def skip_rate(df):
    # Apply the calculate_power_score function to each row
    df["power_score"] = df.apply(calculate_power_score, axis=1)

    # Calculate skip rate
    skip_rate = df["skipped"].mean()

    # Calculate average power score
    avg_power_score = df["power_score"].mean()

    return skip_rate, avg_power_score


def listening_duration(df):
    # Convert ms_played to minutes
    df["minutes_played"] = df["ms_played"] / (1000 * 60)

    # Calculate total listening duration
    total_duration = df["minutes_played"].sum()

    # Calculate average listening duration per track
    avg_duration = df["minutes_played"].mean()

    return total_duration, avg_duration


def shuffle_vs_intentional(df):
    # Count occurrences of shuffle and intentional plays
    shuffle_count = df["shuffle"].sum()
    intentional_count = len(df) - shuffle_count

    # Calculate percentages
    total_plays = len(df)
    shuffle_percentage = (shuffle_count / total_plays) * 100
    intentional_percentage = (intentional_count / total_plays) * 100

    return shuffle_percentage, intentional_percentage


if __name__ == "__main__":
    # Assuming get_json_data() is available from get_data.py
    from get_data import get_spotify

    # Load data into a DataFrame
    df = pd.DataFrame(get_spotify())

    # Convert timestamp to datetime
    df["ts"] = pd.to_datetime(df["ts"])

    # Calculate and print results
    skip_rate_value, avg_power_score = skip_rate(df)
    total_duration, avg_duration = listening_duration(df)
    shuffle_percentage, intentional_percentage = shuffle_vs_intentional(df)

    print(f"Skip Rate: {skip_rate_value:.2%}")
    print(f"Average Power Score: {avg_power_score:.2f}")
    print(f"Total Listening Duration: {total_duration:.2f} minutes")
    print(f"Average Listening Duration per Track: {avg_duration:.2f} minutes")
    print(f"Shuffle Percentage: {shuffle_percentage:.2%}")
    print(f"Intentional Play Percentage: {intentional_percentage:.2%}")
