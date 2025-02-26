from django.contrib import admin
from .models import *

# admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Genre)
admin.site.register(TrackGenre)
admin.site.register(Like)
admin.site.register(ListeningHistory)