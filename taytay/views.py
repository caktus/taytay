from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from taytay.models import Song
import markovify


def make_markov_chain(album):
    lyrics = ""
    if album is not None:
        qs = Song.objects.filter(album__title=album)
    else:
        qs = Song.objects.all()
    for i in qs:
        lyrics += i.lyrics

    lyrics_generator = markovify.text.NewlineText(lyrics, state_size=2)
    return lyrics_generator


def make_stanza(lyrics_generator):
    stanza = ""
    for _ in range(4):
        while True:
            line = lyrics_generator.make_sentence()
            if line is not None:
                stanza += (line + "\n")
                break
    return stanza


def make_song(album=None):
    lyrics_generator = make_markov_chain(album)
    chorus = make_stanza(lyrics_generator)
    song = (make_stanza(lyrics_generator) + "\n \n" + chorus + "\n \n" +
            make_stanza(lyrics_generator) + "\n \n" + chorus +
            "\n \n" + make_stanza(lyrics_generator))
    return song


def make_title(song):
    while True:
        title_generator = markovify.text.NewlineText(song)
        title = title_generator.make_sentence()
        if title is not None:
            title_list = title.split(" ")
            title = " ".join(title_list[0:3])
            return title

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
    album = None
    context = {
        'song': '',
        'title': '',
    }
    if request.method == 'POST':
        title = request.session.get('title')
        song = request.session.get('song')
        if title and song:
            new_song = models.UserSong.objects.create(title=title, lyrics=song)
            return redirect(new_song)
    form = SongForm(request.GET)
    if form.is_valid():
        album = form.cleaned_data['album'].title
    song = make_song(album=album)
    context['song'] = song
    context['title'] = make_title(song)
    context['form'] = form
    request.session['title'] = context['title']
    request.session['song'] = song
    return render(request, 'taytay/song-generator.html', context)


def song_detail(request, slug):
    """Show the details of a saved song."""
    song = get_object_or_404(models.UserSong, slug=slug)
    context = {'song': song}
    return render(request, 'taytay/song-detail.html', context)
