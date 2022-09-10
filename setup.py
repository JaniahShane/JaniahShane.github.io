from http.client import ACCEPTED
from typing import Any
from build_description import build_description
import config
from services.get_spotify import get_spotify
from classes.artistClass import artistClass
from classes.playlistClass import playlistClass
from classes.albumClass import albumClass
from classes.userClass import userClass
from rich import print


spotify = get_spotify()


def main():

    #ask for a country
    print("All")

    country = input()

    if country.uppper() == "All":
        country = None

    #ask for filter by your user styles
    print(" DO YOU WANT TO FILTER BY YOUR TOP GENRES. ('Y' or 'N')")
    print('Y')
    filter_by_genre = input()

    #print("new_albums.setup main...")

    album = albumClass(spotify)

    #get albums list
    processed_albums = album.get_new_album_ids(country, filter_by_genre)

    track_ids = []

    for album_id in [x["id"] for x in processed_albums.accepted]:
        # print(album_id)
        track_ids.extend(album.get_track_ids_for_album(album_id))

        track_id_list = []

        #split track ids into lists of size 100
        for i in range(0, len(track_ids), 100):
            track_id_list.append(track_ids[i : i + 100])

        #results display screen

    if filter_by_genre.upper() == "Y":
        print("=============================================")
        print(" MY TOP GENRE LIST")
        print("=============================================")

        user = userClass(spotify)
        user.set_user_top_genres()
        print(f"+ {user.genres}")

    print("=============================================")
    print(" ACCEPTED")
    print("=============================================")

    for album in processed_albums.accepted:
        print(f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}")

    if filter_by_genre.upper() == "Y":
        print("=============================================")
        print(" REJECTED BECAUSE OF MY TOP GENRE LIST")
        print("=============================================")
        for album in processed_albums.rejected_by_my_top:
            print(
                f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}"
            )
            
    print("=============================================")
    print(" REJECTED BY GENRE FIAT")
    print("=============================================")
    for album in processed_albums.rejected_by_genre:
        print(f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}")

    # Sending to spotify

    # print(result)     

    print("=============================================")
    print(f"updating spotify playlist for {config.SPOTIFY_USER}...")

    # empty playlist first
    result = spotify.user_playlist_replace_tracks(
        config.SPOTIFY_USER, config.PLAYLIST_ID, []
    )

    # add all of the sublists of track_id_lists
    for sublist in track_id_lists: 
        result = spotify.user_playlist_add_tracks(
            config.SPOTIFY_USER, config.PLAYLIST_ID, sublist
        )

    description = build_description(processed_albums.accepted)

    spotify.user_playlist_change_details(
        config.SPOTIFY_USER, config.PLAYLIST_ID, description=description
    )   

    print("Done!")

    if __name__ == "__main__": 
       main()