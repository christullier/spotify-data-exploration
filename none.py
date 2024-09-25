# getting a gauge on how much data is missing
# i thought some of the podcasts were missing at one point
from get_json import get_json_data

data = get_json_data()
import os

missing_dates: dict[str, int] = {}
missing: list[tuple[str, str]] = []


for song in data:
    title = song.get("master_metadata_track_name")
    podcast = song.get("episode_show_name")
    artist = song.get("master_metadata_album_artist_name")
    # if (song == None) & (podcast == None):

    if not artist and not podcast:
        # Get the date of the song (timestamp)
        date = song.get("ts").split("T")[0]

        # Increment the count for this date in the missing_dates dictionary
        # If this date is new, initialize its count to 1; otherwise, increment the existing count
        if date not in missing_dates.keys():
            missing_dates[date] = 1
        else:
            missing_dates[date] += 1

        # Add this song to the list of missing songs
        missing.append(song)

for date in missing_dates:
    if missing_dates[date] > 5:
        print(date, missing_dates[date])
print(len(missing))
