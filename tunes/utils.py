from tunes.models import Song, Artist


def save_spotify_track(track, artists, spotify_link):
    artist, created = Artist.objects.get_or_create(name=artists[0])
    try:
        song = Song.objects.get(title__iexact=track.name, artist=artist)
    except Song.DoesNotExist:
        song = Song()
        song.title = track.name
        song.artist = artist
        song.spotify = True
        song.link = spotify_link
        song.save()
