import csv
import datetime
from django.db import models



class SnippetManager(models.Manager):

    def refresh_colours(self):
        for snippet in self.all():
            snippet.colour = ""
            snippet.save()


class SongManager(models.Manager):

    def export_songs(self):
        export_filename = '/Users/mac/Downloads/songs_export_%s.csv' % datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        with open(export_filename, 'wb') as export_file:
            csvwriter = csv.writer(export_file, delimiter=b',', quotechar=b'"')
            csvwriter.writerow(
                ['id', 'title', 'link', 'created']
            )
            for song in self.all():
                csvwriter.writerow([str(song.id).encode('utf-8'),
                                    str(song.title).encode('utf-8'),
                                    str(song.link).encode('utf-8'),
                                    str(song.created).encode('utf-8'),
                                    ])

    def import_songs(self):
        from .models import Song
        export_filename = '/Users/mac/Downloads/songs_export_20160807103959.csv'
        with open(export_filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                title = row[1]
                if title:
                    try:
                        song = self.get(title=title)
                    except Song.DoesNotExist:
                        self.create(
                            title=row[1],
                            link=row[2],
                            created=row[3]
                        )


class EntryManager(models.Manager):

    def list_entries(self):
        return self.filter(name__startswith="Ben")
