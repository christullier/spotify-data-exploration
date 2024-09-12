# getting a gauge on how much data is missing
# i thought some of the podcasts were missing at one point
from get_json import get_json_data

data = get_json_data()
import os

missing_dates = {}
missing = []


for song in data:
    title = song.get("master_metadata_track_name")
    podcast = song.get("episode_show_name")
    artist = song.get("master_metadata_album_artist_name")
    # if (song == None) & (podcast == None):
    if not artist and not podcast:
        date = song.get("ts").split("T")[0]
        if date not in missing_dates.keys():
            missing_dates[date] = 1
        else:
            missing_dates[date] += 1

        missing.append(song)
        # print(song)
        # input()
        # os.system("clear")


for date in missing_dates:
    if missing_dates[date] > 5:
        print(date, missing_dates[date])
print(len(missing))
