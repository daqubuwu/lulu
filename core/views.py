from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model


User = get_user_model()

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

def track_detail(request, track_id):
    track = Track.objects.get(id=track_id)
    genres = track.trackgenre_set.all()
    context = {
        'track': track,
        'genres': genres,
    }
    return render(request, 'track_detail.html', context)




@login_required
def favorites(request):
    liked_tracks = Like.objects.filter(user=request.user).select_related('track')
    tracks = [like.track for like in liked_tracks]
    context = {
        'tracks': tracks,
    }
    return render(request, 'favorites.html', context)

def history(request):
    return render(request, 'history.html')

def register(request):
    return render(request, 'core_auth/register.html')

def login(request):
    return render(request, 'core_auth/login.html')


def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    genres = track.trackgenre_set.all()
    liked_tracks = []
    if request.user.is_authenticated:
        # user = User.objects.get(user=request.user)
        print("ksjdbfjkehjdfhgjdhfjk",request.user)
        liked_tracks = Like.objects.filter(user=request.user).values_list('track_id', flat=True)
    context = {
        'track': track,
        'genres': genres,
        'liked_tracks': liked_tracks,
    }
    return render(request, 'track_detail.html', context)

@login_required
def like_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    user = User.objects.get(username=request.user.username)
    like, created = Like.objects.get_or_create(user=user, track=track)
    if not created:
        like.delete()
    return redirect('track_detail', track_id=track_id)