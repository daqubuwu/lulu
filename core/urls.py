from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('artist_detail/', views.Artist, name='artists'),
        path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('tracks/', views.tracks, name='tracks'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)