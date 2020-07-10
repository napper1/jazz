import csv

import datetime
import json
import os
import pdb

import ffmpeg
import requests
from background_task import background
from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template.loader import get_template
from django.utils.text import slugify
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag
from weasyprint import CSS, HTML
from weasyprint.fonts import FontConfiguration

from .forms import SongForm, ManySelectForm, MediaForm
from .models import Song, Artist, SongDocument
from youtube_api.models import Video


def index(request):
    form = SongForm()
    songs = Song.objects.all().order_by('title')
    context = dict()
    if request.method == "POST":
        # add song
        form = SongForm(data=request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            if form.cleaned_data.get('artist'):
                artist_name = form.cleaned_data['artist']
                try:
                    artist = Artist.objects.get(name=artist_name)
                except Artist.DoesNotExist:
                    artist = Artist.objects.create(name=artist_name)
                song.artist = artist
            song.save()
            form.save_m2m()
            messages.success(request, "Song added!")
        else:
            messages.error(request, "Please check the form errors and try again.")
    context['form'] = form
    context['songs'] = songs.order_by('-created')
    context['artists'] = Artist.objects.all().prefetch_related('songs')
    context['tags'] = Tag.objects.all()
    context['recently_added'] = songs.order_by('-created')[:5]
    context['uplifting_songs'] = songs.filter(tags__name='Uplifting')
    return render(request, "tunes/index.html", context)


def test(request):
    context = dict()
    form = ManySelectForm()
    if request.method == "POST":
        form = ManySelectForm(data=request.POST)
        if form.is_valid():
            songs = form.cleaned_data.get("songs")
            for song in songs:
                print(song)
    context['checkbox_form'] = form
    return render(request, "tunes/test.html", context)


@csrf_exempt
def add_song(request):
    """
    Ajax add song.
    """
    data = dict()
    if request.method == "POST":
        post_data = json.loads(request.body)
        form = SongForm(data=post_data)
        if form.is_valid():
            song = form.save(commit=False)
            if form.cleaned_data.get('artist'):
                artist_name = form.cleaned_data['artist']
                # artist_names = Artist.object.all().values_list("name", flat=True)
                # if artist_name in artist_names:
                #     data['response'] = False
                #     data['errors'] = 'This artist already exists'
                try:
                    artist = Artist.objects.get(name__iexact=artist_name)
                except Artist.DoesNotExist:
                    artist = Artist.objects.create(name=artist_name)
                song.artist = artist
            # if form.cleaned_data.get('url'):
            #     song.link = form.cleaned_data['url']
            song.save()
            form.save_m2m()
            data['response'] = True
            data['song_id'] = song.id
            data['title'] = song.title
            data['link'] = song.link
        else:
            data['response'] = False
            data['errors'] = form.errors
        return JsonResponse(data=data)
    return HttpResponse()


@csrf_exempt
def get_next_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    # find the next song which is the previous ID
    next_song = Song.objects.filter(id__lt=song.id).order_by('id').last()
    data = next_song.to_json()
    return JsonResponse(data)


@csrf_exempt
def lookup_song(request):
    q = request.GET.get("q")
    data = []
    if q:
        songs = Song.objects.filter(Q(title__icontains=q) | Q(artist__name__icontains=q))
        for song in songs:
            res = song.to_json()
            data.append(res)
    return JsonResponse(data, safe=False)


@csrf_exempt
def remove_song(request):
    data = dict()
    if request.is_ajax():
        song_id = request.POST.get('song_id')
        if song_id:
            try:
                song = Song.objects.get(id=song_id)
            except Song.DoesNotExist:
                pass
            else:
                song.delete()
                data['response'] = True
        return JsonResponse(data=data)


@csrf_exempt
def update_last_played(request, song_id):
    if request.is_ajax():
        song = get_object_or_404(Song, id=song_id)
        song.last_played = now()
        song.save()
        return JsonResponse({"response": "ok"})
    return JsonResponse({"response": "fail"})


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_music(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    if request.method == "GET":
        qs = Song.objects.all().order_by('title')
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(get_row(obj)) for obj in qs), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="my-songs-export-%s.csv"' % datetime.datetime.now()
        return response
    return redirect(index)


def get_row(obj):
    row = [
        str(obj.id).encode('utf-8'),
        str(obj.title).encode('utf-8'),
        str(obj.link).encode('utf-8'),
        str(obj.tab_link).encode('utf-8'),
    ]
    return row

#### Using Asynchronous method ####

# from tasks import generate_file
#
#
# def export(request, **kwargs):
#     task = generate_file.delay(**kwargs)
#     return render_to_response("poll_for_download.html", {"task_id": task.task_id })


@csrf_exempt
def get_artist_songs(request):
    data = dict()
    if request.is_ajax():
        name = request.GET.get("name")
        if name:
            songs = Song.objects.filter(artist__name__icontains=name).values('id', 'title', 'artist__name', 'link')
            data['songs'] = list(songs)
    return JsonResponse(data=data)


@csrf_exempt
def search_youtube(request):
    data = dict()
    if request.is_ajax():
        name = request.GET.get("name")
        if name:
            videos = Video.remote.search(name)
            videos = videos[:10]
            videos_list = list()
            for video in videos:
                url = "https://youtube.com/" + video.slug
                videos_list.append({'title': video.title, 'url': url, 'thumbnail': video.get_thumbnail_medium})
            data = videos_list
    return JsonResponse(data=data, safe=False)


@csrf_exempt
def suggestions(request):
    artists = Artist.objects.values_list('name', flat=True)
    return JsonResponse(data=list(artists), safe=False)


@csrf_exempt
def download_link(request, song_id):
    if request.method == "POST":
        song = get_object_or_404(Song, id=song_id)
        mkv_file_path = song.convert_to_mkv()
        mkv_file_path += ".mkv"
        print(mkv_file_path)
        # convert from mvk to mp3 using ffmpeg
        stream = ffmpeg.input(mkv_file_path)
        filename = '%s-%s.%s' % (slugify(song.title), song.artist.name, 'mp3')
        file_path = os.path.join(settings.YOUTUBE_EXPORT_PATH, filename)
        stream = ffmpeg.output(stream, file_path, acodec='libmp3lame')
        ffmpeg.run(stream)
        song.downloaded = True
        song.save()
        print(file_path)
        os.remove(mkv_file_path)
        return JsonResponse(data={'result': 'ok', 'path': file_path}, safe=False)
    return JsonResponse(data={"result": "fail"}, safe=False)


def experiment(request):
    form = MediaForm()
    return render(request, 'tunes/experiment_two.html', {'form': form})


def pdf(request):
    from io import BytesIO

    url = 'https://www.asx.com.au/asxpdf/20171108/pdf/43p1l61zf2yct8.pdf'
    response = requests.get(url)
    my_raw_data = response.content

    pdf_content = BytesIO(my_raw_data)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf'
    return response


def test_pdf(request):
    t = get_template('tunes/weasyprint.html')
    html = t.render({})
    font_config = FontConfiguration()
    css = CSS(settings.BASE_DIR + '/tunes/static/css/weasyprint.css', font_config=font_config)
    pdf_file = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css],
                                                                                  font_config=font_config,
                                                                                  presentational_hints=True)
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename=boy_%s_reports.pdf'
    return http_response


def test_html(request):
    return render(request, 'tunes/weasyprint.html', {'print': True})


@csrf_exempt
def save_document(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        document = request.FILES.get("file")
        document_two = request.FILES.get("file_second")
        groups_file = request.FILES.get('groups')
        groups_string = groups_file.read().decode('utf-8')
        groups = json.loads(groups_string)
        song_doc = SongDocument()
        if document:
            song_doc.document = document
        if document_two:
            song_doc.document_two = document_two
        if groups:
            song_doc.data = groups
        song_doc.save()
        if document or save_document:
            data = {'response': 'success'}
        else:
            data = {'response': 'fail'}
        return JsonResponse(data)
    return Http404()


@background()
def backup_database():
    call_command("dbbackup")


@csrf_exempt
def backup_music(request):
    # run a task in the background to backup the database to Dropbox
    backup_database()
    return JsonResponse({"response":"success"})
