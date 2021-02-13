from django.contrib import admin
from .models import Song, Artist, YoutubeVideo, SongDocument, SongCategory


class SongAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created',
        'modified',
        'artist',
        'link',
        'tab_link',
        'last_played',
        'is_favourite',
    )
    list_filter = ('created', 'modified', 'last_played', 'is_favourite')
    raw_id_fields = ('artist',)
    search_fields = ['title']


class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'value')


class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = [
        'video_id',
        'video_title',
        'labeled',
    ]
    search_fields = [
        'video_id',
        'video_title',
    ]
    list_editable = [
        'labeled',
    ]


class SongDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'document_two', 'data']


class SongCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title']


admin.site.register(Song, SongAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
admin.site.register(SongDocument, SongDocumentAdmin)
admin.site.register(SongCategory, SongCategoryAdmin)
