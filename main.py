import json
from os import getenv

from dotenv import load_dotenv

load_dotenv()

root_dir = getenv("EXTENDED_HISTORY_FILES_DIR")

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


total_time = 0
artists = {}

for json_file in files:
    # print(json_file)
    with open(f"{root_dir}{json_file}") as f:
        d: dict[dict] = json.load(f)
        for song in d:
            ms = song.get("ms_played")
            total_time += ms
            artist = song.get("master_metadata_album_artist_name")
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

sorted = dict(sorted(artists.items(), key=lambda item: item[1]))

print(sorted)
