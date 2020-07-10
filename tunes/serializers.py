from rest_framework import serializers
from rest_framework.fields import CharField

from tunes.models import Artist, Song


class ArtistSerializer(serializers.ModelSerializer):

    song_count = CharField()

    class Meta:
        model = Artist
        fields = ['id',
                  'name',
                  'song_count']


class SongSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['id',
                  'title',
                  'artist',
                  'link',
                  'last_played',
                  'is_favourite',
                  'admin_link',
                  'download_link',
                  'media_link',
                  'downloaded',
                  'created',
                  ]
