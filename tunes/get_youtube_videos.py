from django.conf import settings
from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
import os
import json

from tunes.models import YoutubeVideo

DEVELOPER_KEY = settings.YOUTUBE_API_ACCESS_KEY


def html_reverse_escape(string):
    '''Reverse escapes HTML code in string into ASCII text.'''
    # see Ned Batchelder post https://stackoverflow.com/questions/2077283/escape-special-html-characters-in-python
    return (string \
        .replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"'))


def search_api(search_query, max_results=20):
    '''Searches YouTube Data API v3 for videos based on project-specified parameters; returns list of videos.'''

    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = build(api_service_name, api_version,
                        developerKey = DEVELOPER_KEY)
    # limit results to 20 and only query non-copyright videos
    request = youtube.search().list(
            part='id,snippet',
            maxResults=max_results,
            q=search_query,
            relevanceLanguage='en',
            type='video',
            videoDuration='medium',
            videoLicense='creativeCommon',
            videoSyndicated='true',
        ).execute()
    for search_result in request['items']:
        video_title = search_result['snippet']['title']
        video_title = html_reverse_escape(video_title)
        video_id = search_result['id']['videoId']
        video_description = search_result['snippet']['description']
        if video_title and video_description and video_id:
            try:
                new_video = YoutubeVideo.objects.get(video_id=video_id)
            except YoutubeVideo.DoesNotExist:
                new_video = YoutubeVideo()
            new_video.video_id = video_id
            new_video.video_title = video_title
            new_video.video_description = video_description
            new_video.save()
