import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius

token = "your_token"
client_id = "your_client_id"
client_secret = "your_client_secret"


def authenticate_spotify():
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


def get_artist_id(spotify, artist_name):
    results = spotify.search(q=artist_name, type='artist')
    return results['artists']['items'][0]['id'] if results['artists']['items'] else None


def get_albums(spotify, artist_id):
    return spotify.artist_albums(artist_id, album_type='album', limit=50)


def display_albums(albums):
    print("Az előadó összes albuma:")
    album_names = [album['name'] for album in albums['items']]
    # Az enumerate az albumok számozásásra szolgál
    for i, album_name in enumerate(album_names, start=1):
        print(f"{i}. {album_name}")
    return album_names


def select_album():
    selected_album_index = int(input("\nHányas számú albumra vagy kíváncsi?\n")) - 1
    return selected_album_index


def get_tracks(spotify, album_id):
    return spotify.album_tracks(album_id)


def display_tracks(tracks):
    print("Az album dalai:")
    track_names = [track['name'] for track in tracks['items']]
    for idx, track_name in enumerate(track_names, start=1):
        print(f"{idx}. {track_name}")
    return track_names


def select_track():
    selected_track_index = int(input("\nVálassz egy számot a dalok közül:\t")) - 1
    return selected_track_index


def get_lyrics(song_name, artist_name):
    genius = lyricsgenius.Genius(token)
    song = genius.search_song(song_name, artist_name)
    return song.lyrics


def main():
    print("Ezzel a programmal kiderítheted a kedvenc dalaid dalszövegét!")
    spotify = authenticate_spotify()
    while True:
        artist_name = input("Add meg a kedvenc előadód teljes nevét!:\t")
        artist_id = get_artist_id(spotify, artist_name)

        albums = get_albums(spotify, artist_id)
        album_names = display_albums(albums)
        selected_album_index = select_album()
        selected_album_id = albums['items'][selected_album_index]['id']
        tracks = get_tracks(spotify, selected_album_id)
        track_names = display_tracks(tracks)
        selected_track_index = select_track()
        selected_track = tracks['items'][selected_track_index]
        lyrics = get_lyrics(selected_track['name'], artist_name)

        if lyrics:
            print(f"\n{selected_track['name']} szövege:")
            print(lyrics)
        if input("\nKíváncsi vagy még több dalra? (I/N)") != "I":
            break


main()
