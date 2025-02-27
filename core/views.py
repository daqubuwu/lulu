from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random

User = get_user_model()


def home(request):
    new_tracks = list(Track.objects.all())
    random.shuffle(new_tracks)

    recommended_tracks = list(Track.objects.all())
    random.shuffle(recommended_tracks)
    recommended_tracks = recommended_tracks[:5]

    unusual_playlists = list(Playlist.objects.all())
    random.shuffle(unusual_playlists)

    all_playliists = list(Playlist.objects.all())
    all_playlists = all_playliists[:4]

    context = {
        'new_tracks': new_tracks,
        'recommended_tracks': recommended_tracks,
        'unusual_playlists': unusual_playlists,
        'all_playlists': all_playlists,
    }
    return render(request, 'home.html', context)


def artist_detail(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    albums = Album.objects.filter(artist=artist)
    tracks = Track.objects.filter(artist=artist)
    return render(request, 'artist_detail.html', {'artist': artist, 'albums': albums, 'tracks': tracks})


def tracks(request):
    tracks = Track.objects.select_related('artist').all()
    return render(request, 'main/tracks.html', {'tracks': tracks})


def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    genres = track.trackgenre_set.all()
    liked_tracks = []
    if request.user.is_authenticated:
        liked_tracks = Like.objects.filter(user=request.user).values_list('track_id', flat=True)
    context = {
        'track': track,
        'genres': genres,
        'liked_tracks': liked_tracks,
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


def register(request):
    return render(request, 'core_auth/register.html')


def login(request):
    return render(request, 'core_auth/login.html')


@login_required
def like_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    user = User.objects.get(username=request.user.username)
    like, created = Like.objects.get_or_create(user=user, track=track)
    if not created:
        like.delete()
    return redirect('track_detail', track_id=track_id)


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    context = {
        'playlist': playlist,
    }
    return render(request, 'playlist_detail.html', context)