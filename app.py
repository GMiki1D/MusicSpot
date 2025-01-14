import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, jsonify, render_template

# Flask app initialization
app = Flask(__name__)

# Spotify API Credentials
SPOTIFY_CLIENT_ID = "f7da951421454e2db2dd4f3d5962b835"
SPOTIFY_CLIENT_SECRET = "73843ff6b00649219698721a70fe0efe"

# Initialize Spotify client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

def fetch_random_track(artist):
    """Fetch a random track for the given artist using the Spotify API."""
    try:
        result = sp.search(q=artist, limit=1, type='artist')
        if not result['artists']['items']:
            return None, "Nem találtunk ilyen néven előadót :("

        artist_id = result['artists']['items'][0]['id']

        # Get all albums (including singles)
        albums = sp.artist_albums(artist_id, album_type='album,single')['items']
        all_tracks = []

        # Loop through each album and get the tracks
        for album in albums:
            album_tracks = sp.album_tracks(album['id'])['items']
            for track in album_tracks:
                all_tracks.append({
                    "name": track['name'],
                    "url": track['external_urls']['spotify'],
                    "image": album['images'][0]['url'] if album['images'] else None
                })

        if not all_tracks:
            return None, "Nincsenek elérhető számok az előadótól."

        # Choose a random track
        random_track = random.choice(all_tracks)
        track_data = {
            "title": random_track["name"],
            "url": random_track["url"],
            "image": random_track["image"]
        }
        return track_data, None
    except Exception as e:
        return None, str(e)


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/get-track", methods=["POST"])
def get_track():
    """Handle requests for random tracks."""
    artist = request.form.get("artist")
    if not artist:
        return jsonify({"error": "Kérlek adj meg egy előadót!"}), 400

    track, error = fetch_random_track(artist)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(track)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443)
