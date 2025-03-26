import json
from os import getenv
import csv
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SPOTIFY_DIR = getenv("SPOTIFY_DIR")
APPLE_DIR = getenv("APPLE_DIR")


def read_json(file_names):
    json_data = []
    for json_file in file_names:
        print(f"{json_file=}")
        with open(json_file) as f:
            new_data = json.load(f)
            json_data.extend(new_data)

    return json_data


def read_csv(file_names):
    # csv_data = []
    for csv_filename in file_names:
        df = pd.read_csv(csv_filename)
        # csv_data.extend(df)
    return df


def get_spotify():
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

    file_paths = [f"{SPOTIFY_DIR}/{file}" for file in files]

    json_data = read_json(file_paths)
    return json_data


def apple_fp() -> str:
    file = "Apple Music Play Activity.csv"
    file_path = f"{APPLE_DIR}/{file}"
    return file_path


if __name__ == "__main__":
    # d = get_spotify_json()
    d = get_apple()
    print(len(d))
