import json
from os import getenv

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
