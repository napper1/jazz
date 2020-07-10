from django.conf.urls import url
from django.views.generic import TemplateView

from tunes import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^api-add-song/$', views.add_song, name='add_song'),
    url(r'^api-remove-song/$', views.remove_song, name='remove_song'),
    url(r'^api-update-last-played/(?P<song_id>\d+)/$', views.update_last_played, name='update_last_played'),
    url(r'^export-songs/$', views.export_music, name='export_songs'),
    url(r'^test/$', views.test, name='test'),
    url(r'^get_artist_songs/$', views.get_artist_songs, name='get_artist_songs'),
    url(r'^search_youtube/$', views.search_youtube, name='search_youtube'),
    url(r'^suggestions/$', views.suggestions, name='suggestions'),
    url(r'^download/(?P<song_id>\d+)/$', views.download_link, name='download_link'),
    url(r'^experiment/$', views.experiment, name='experiment'),
    url(r'^pdf/$', views.pdf, name='pdf'),
    url(r'^test-pdf/$', views.test_pdf, name='test_pdf'),
    url(r'^test-html/$', views.test_html, name='test_html'),
    url(r'^api-document/$', views.save_document, name='save_document'),
    url(r'^api-get-next/(?P<song_id>\d+)/$', views.get_next_song, name='get_next_song'),
    url(r'^api/lookup-song/$', views.lookup_song, name='lookup_song'),
    url(r'^api/backup-music/$', views.backup_music, name='backup_music'),

    # url(r'^test/$', TemplateView.as_view(template_name='test.html'), name='suggestions'),

]
