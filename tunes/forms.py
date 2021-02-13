from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Song, MediaFile


class SongForm(forms.ModelForm):

    artist = forms.CharField(label="Artist", max_length=100)

    class Meta:
        model = Song
        fields = ('title', 'link', 'tags', 'category', )


class ManySelectForm(forms.Form):

    songs = forms.ModelMultipleChoiceField(queryset=Song.objects.all(),
                                           widget=CheckboxSelectMultiple())


class MediaForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['media_type']
