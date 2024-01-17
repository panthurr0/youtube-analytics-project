import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']
        self.description = self.channel['items'][0]['snippet']['description']

    @classmethod
    def get_service(cls):
        """
        :return: Объект, для работы с YT API.
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    def print_info(self):
        """
        Выводит информацию о канале на экран.
        """
        print(self.channel)

    def to_json(self, filename):
        """
        Записывает информацию о канале в json-файл.
        """
        result = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber,
            'video_count': self.video_count,
            'view_count': self.viewCount
        }
        file = open(filename, 'w')
        json.dump(result, file)
        file.close()

    @property
    def channel_id(self):
        return self.__channel_id
