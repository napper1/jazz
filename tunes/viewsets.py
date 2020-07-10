from datetime import timedelta

from django.db.models import Q
from django.utils.timezone import now
from rest_framework import viewsets

from tunes.models import Artist, Song
from tunes.serializers import ArtistSerializer, SongSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing artists.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_queryset(self):
        qs = self.queryset
        letter = self.request.GET.get('letter')
        if letter:
            return qs.filter(name__istartswith=letter)
        return qs


class SongViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing artists.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_fields = ('is_favourite',)

    def get_queryset(self):
        qs = self.queryset
        artist = self.request.GET.get('artist')
        q = self.request.GET.get('q')
        show = self.request.GET.get('show')
        search_yt = self.request.GET.get('search_yt')
        limit = self.request.GET.get("limit")
        if artist:
            qs = qs.filter(artist=artist)
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(artist__name__icontains=q))[:10]
        if show == 'recent':
            three_months_ago = now() - timedelta(days=90)
            qs = qs.filter(created__gt=three_months_ago).order_by('-created')
        elif show == 'last_played':
            qs = qs.filter(last_played__isnull=False).order_by('-last_played')[:5]
        if limit == "short":
            qs = qs[:5]
        return qs