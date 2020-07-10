import youtube_dl
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

from .managers import SongManager, EntryManager
from django.conf import settings
from youtube_api.models import Video
import os

# Control the file name structure with output templates (see docs)
YOUTUBE_EXPORT_DEFAULT_PATH = os.path.join(settings.YOUTUBE_EXPORT_PATH, '%(title)s-%(id)s.%(ext)s')


class Song(TimeStampedModel):
    title = models.CharField("Name", max_length=200)
    artist = models.ForeignKey("Artist", related_name='songs', null=True, on_delete=models.CASCADE)
    link = models.CharField("YouTube", max_length=200, null=True, blank=True)
    tab_link = models.CharField("Guitar", max_length=200, null=True, blank=True)
    last_played = models.DateTimeField(null=True, blank=True)
    is_favourite = models.BooleanField("Is Favourite?", default=False)
    downloaded = models.BooleanField("Downloaded?", default=False)

    tags = TaggableManager(blank=True)

    objects = SongManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    @property
    def admin_link(self):
        return reverse('admin:tunes_song_change', args=[self.id])

    @property
    def download_link(self):
        return reverse('download_link', args=[self.id])

    @property
    def media_link(self):
        return settings.YOUTUBE_EXPORT_URL + '/' + slugify(self.title) + ".mp3"

    def save(self, **kwargs):
        # if not self.link:
        #     # try getting it from youtube
        #     try:
        #         video = Video.remote.search(self.title)[0]
        #     except IndexError:
        #         pass
        #     else:
        #         self.link = "https://www.youtube.com/watch?v=%s" % video.video_id
        super(Song, self).save(**kwargs)

    def get_video_id(self):
        if self.link:
            link = self.link.split('?v=')
            if len(link) == 2:
                video_id = link[1]
                return video_id
        return

    def get_thumbnail(self):
        # ping YouTube for thumbnail
        image = ""
        video_id = self.get_video_id()
        if video_id:
            try:
                video = Video.objects.get(video_id=video_id)
            except Video.DoesNotExist:
                try:
                    video = Video.remote.fetch(video_id)[0]
                except IndexError:
                    return None
            if hasattr(video, "thumbnail_urls"):
                if video.thumbnail_urls.get("high"):
                    image = video.thumbnail_urls.get("high")
                else:
                    image = video.thumbnail_urls.get("default")
                return image
        return image

    def get_published_at(self):
        video = self.get_video()
        if video:
            return video.published_at

    def get_video(self):
        video_id = self.get_video_id()
        if video_id:
            try:
                video = Video.objects.get(video_id=video_id)
            except Video.DoesNotExist:
                try:
                    video = Video.remote.fetch(video_id)[0]
                except IndexError:
                    pass
                else:
                    return video
            else:
                return video

    def convert_to_mp3(self):
        """
        Use the youtube-dl package to convert the link to mp3.
        :return:
        """
        # filename = '%(title)s.%(ext)s' % (title=self.title, ext=3)
        filename = '%s-%s.%s' % (slugify(self.title), self.artist.name, 'mp3')
        ydl_opts = {
            'verbose': True,
            'fixup': 'detect_or_warn',  # Automatically correct known faults of the file.
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'audioformat': 'best',
            'extractaudio' : True,      # only keep the audio
            'recodevideo': 'webm',
            'prefer-avconv': True,
            # 'outtmpl': YOUTUBE_EXPORT_DEFAULT_PATH
            'outtmpl': os.path.join(settings.YOUTUBE_EXPORT_PATH, filename)
        }
        ydl_opts = {}
        print(self.link)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link])
        return

    def convert_to_mkv(self):
        filename = '%s-%s.%s' % (slugify(self.title), self.artist.name, 'mkv')
        file_path = os.path.join(settings.YOUTUBE_EXPORT_PATH, filename)
        ydl_opts = {
            'outtmpl': file_path
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link])
        return file_path

    def to_json(self):
        data = dict()
        data['id'] = self.id
        data['title'] = self.title
        data['artist'] = self.artist.name
        data['link'] = self.link
        return data


class Artist(models.Model):
    name = models.CharField("Name", max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def song_count(self):
        return self.songs.all().count()


MOOD_CHOICES = (
    ('HAPPY', 'Happy'),
    ('IN-LOVE', 'In-Love'),
    ('SAD', 'Sad'),
    ('CONFIDENT-SASSY', 'Confident-sassy'),
    ('CHILL', 'Chill'),
    ('ANGRY', 'Angry'),
)


class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=11, null=False, blank=True, primary_key=True)
    video_title = models.TextField(db_index=True, null=True, blank=True)
    labeled = models.NullBooleanField()
    video_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.video_title if self.video_title else "No title"


class SongDocument(models.Model):
    document = models.FileField(upload_to='documents')
    document_two = models.FileField(upload_to='documents', null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class MediaFile(models.Model):
    MEDIA_CHOICES = [
        ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
         ),
        ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
         ),
        ('unknown', 'Unknown'),
    ]
    media_type = models.CharField(max_length=20, choices=MEDIA_CHOICES)

    def __str__(self):
        return self.media_type
