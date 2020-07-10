from django import template

from tunes.models import Song

register = template.Library()


@register.inclusion_tag('tunes/includes/show_tagged_songs.html')
def show_tagged_songs(tag):
    songs = Song.objects.filter(tags__in=[tag])
    return {'songs': songs}


@register.simple_tag(takes_context=True)
def show_text(context):
    print(context['my_text'])
    return str(context['my_text'])
