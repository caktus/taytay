from django.shortcuts import render


def song_generator(request):
    """Generate a new song."""
    context = {
        'song': ''
    }
    return render(request, 'taytay/song-generator.html', context)
