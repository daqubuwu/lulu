from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    query = request.GET.get('q')
    if query:
        tracks = Track.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))[:9]
    else:
        tracks = Track.objects.select_related('artist').all()

    artists = Artist.objects.all()
    playlists = Playlist.objects.all()

    return render(request, 'home.html', {'tracks': tracks, 'artists': artists, 'playlists': playlists})

def artist_detail(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    albums = Album.objects.filter(artist=artist)
    tracks = Track.objects.filter(artist=artist)
    return render(request, 'artist_detail.html', {'artist': artist, 'albums': albums, 'tracks': tracks})

def tracks(request):
    tracks = Track.objects.select_related('artist').all()
    return render(request, 'main/tracks.html', {'tracks': tracks})


@login_required
def favorites(request):
    username = ""
    try:
        user = User.objects.get(username=username)
        favorites = Track.objects.filter(like__user=user)
        return render(request, 'favorites.html', {'favorites': favorites})
    except User.DoesNotExist:
        return render(request, 'favorites.html', {'error': 'Пользователь не найден'})

def history(request):
    return render(request, 'history.html')

def register(request):
    return render(request, 'core_auth/register.html')

def login(request):
    return render(request, 'core_auth/login.html')



def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    genres = track.trackgenre_set.all()  # Получаем жанры трека
    context = {
        'track': track,
        'genres': genres,
    }
    return render(request, 'track_detail.html', context)