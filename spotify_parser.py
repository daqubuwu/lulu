import os
import django
import spotipy
import wikipediaapi
import logging
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_app.settings')
django.setup()

from core.models import Artist, Album, Track, Genre, Playlist
from django.contrib.auth.models import User

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Замени на свои client_id и client_secret
client_id = '0c9f137b2f834e9098b1e9830ec07665'
client_secret = '12ecbf1fec3e450eb3391f33d7f77f4e'

# Авторизация в Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Инициализация Wikipedia API с указанием user_agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',  # Указываем язык (например, 'ru' для русского)
    user_agent='YourAppName/1.0 (your@email.com)'  # Указываем user_agent
)


def get_artist_bio(artist_name):
    """
    Получает биографию артиста с Wikipedia.
    """
    page = wiki_wiki.page(artist_name)
    if page.exists():
        return page.summary  # Возвращаем краткое описание
    return ""  # Если страница не найдена, возвращаем пустую строку


def get_top_tracks(total_tracks=100):
    """
    Получает топ-треки из Spotify с использованием пагинации.
    """
    tracks = []
    limit = 50  # Максимальное количество треков за один запрос
    offset = 0

    while len(tracks) < total_tracks:
        results = sp.search(q='year:2023', type='track', limit=limit, offset=offset, market='US')
        tracks.extend(results['tracks']['items'])
        offset += limit

        # Если больше нет треков, прерываем цикл
        if len(results['tracks']['items']) < limit:
            break

    return tracks[:total_tracks]  # Возвращаем только нужное количество треков


def save_tracks_to_db():
    """
    Сохраняет топ-треки в базу данных Django.
    """
    tracks = get_top_tracks(total_tracks=100)
    user = User.objects.first()  # Получаем первого пользователя для плейлистов

    for track_data in tracks:
        # Сохранение артиста
        artist_data = track_data['artists'][0]
        artist_info = sp.artist(artist_data['id'])  # Получаем информацию об артисте

        # Фото артиста (первое изображение из списка)
        artist_photo = artist_info['images'][0]['url'] if artist_info.get('images') else None

        # Биография артиста (получаем с Wikipedia)
        artist_bio = get_artist_bio(artist_data['name'])

        artist, _ = Artist.objects.get_or_create(
            name=artist_data['name'],
            defaults={
                'bio': artist_bio,  # Сохраняем биографию
                'photo': artist_photo  # Сохраняем фото артиста
            }
        )

        # Получение жанров артиста
        for genre_name in artist_info.get('genres', []):
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            artist.genres.add(genre)

        # Сохранение альбома
        album_data = track_data['album']
        cover_url = album_data['images'][0]['url'] if album_data.get('images') else None

        album, _ = Album.objects.get_or_create(
            title=album_data['name'],
            artist=artist,
            defaults={
                'release_date': album_data['release_date'],
                'cover': cover_url
            }
        )

        # Сохранение трека
        track, _ = Track.objects.get_or_create(
            title=track_data['name'],
            artist=artist,
            album=album,
            defaults={
                'duration': track_data['duration_ms'] // 1000,  # Переводим миллисекунды в секунды
                'file_url': track_data.get('preview_url')  # Используем .get(), чтобы избежать ошибки
            }
        )

        # Создание плейлистов по жанрам
        for genre in artist.genres.all():
            playlist, _ = Playlist.objects.get_or_create(
                title=f"{genre.name} Hits",
                user=user,
                defaults={'description': f"Лучшие треки в жанре {genre.name}"}
            )
            playlist.tracks.add(track)

    print(f"Успешно сохранено {len(tracks)} треков в базу данных!")


if __name__ == '__main__':
    save_tracks_to_db()