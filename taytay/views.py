from django import forms
from django.shortcuts import render

from . import models


class SongForm(forms.ModelForm):
    """Choices for song generation."""

    class Meta:
        model = models.Song
        fields = ('album', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].empty_label = 'Select an album...'
        self.fields['album'].label = 'Generate Based on an Album'
        self.fields['album'].to_field_name = 'slug'


def song_generator(request):
    """Generate a new song."""
    context = {
        'song': '',
        'albums': '',
    }
    form = SongForm(request.GET)
    if form.is_valid():
        # TODO: Do something with the selected album
        pass
    context['form'] = form
    return render(request, 'taytay/song-generator.html', context)
