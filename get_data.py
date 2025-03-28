import glob
import json
from os import getenv, path

import pandas as pd
from dotenv import load_dotenv

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

    # Get all Streaming_History_Audio_*.json files from SPOTIFY_DIR
    files = glob.glob(path.join(SPOTIFY_DIR, "Streaming_History_Audio_*.json"))
    file_paths = files

    json_data = read_json(file_paths)
    return json_data


def apple_fp() -> str:
    file = "Apple Music Play Activity.csv"
    file_path = f"{APPLE_DIR}/{file}"
    return file_path


if __name__ == "__main__":
    d = get_spotify()
    # d = get_apple()
    print(len(d))
