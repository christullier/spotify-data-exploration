from get_json import get_json_data

total_time = 0
song_plays = {}
artists = {}

for song in get_json_data():
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
