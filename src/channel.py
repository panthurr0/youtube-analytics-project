import json
import os

from googleapiclient.discovery import build
from helper.youtube_api_manual import api_key


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id

    def get_info(self) -> None:
        """Получает информацию по API."""
        youtube = build('youtube', 'v3', developerKey='AIzaSyAY5JLIJCY00JEf-Ux-lpkDZDcZ6sWOTw8')
        return youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def print_info(self):
        """
        Выводит информацию на экран.
        """
        info = self.get_info()
        print(info)
