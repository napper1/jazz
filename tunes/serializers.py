from rest_framework import serializers
from rest_framework.fields import CharField

from tunes.models import Artist, Song, SongCategory


class ArtistSerializer(serializers.ModelSerializer):

    song_count = CharField()

    class Meta:
        model = Artist
        fields = ['id',
                  'name',
                  'song_count']


class SongCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SongCategory
        fields = ['id', 'title']


class SongSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(read_only=True)
    song_category = serializers.SerializerMethodField()

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
                  'category',
                  'song_category',
                  'spotify',
                  'created',
                  ]

    def get_song_category(self, obj):
        # convert object to JSON serialization
        if obj.category:
            thing = SongCategorySerializer(instance=obj.category)
            return thing.to_representation(obj.category)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.pop('title')
    #     # artist, created = Artist.objects.get_or_create(name__iexact=artist_name)
    #     # instance.artist = artist
    #     artist_id = validated_data.pop('artist')
    #     instance.artist_id = artist_id
    #     instance.link = validated_data.pop('link')
    #     instance.category_id = validated_data.pop('category')
    #     instance.save()
    #     return instance
