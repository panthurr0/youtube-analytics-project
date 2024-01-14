from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey="AIzaSyDYrN5CoB9aNNKdP9HuYXGs8lcn_9jg1Hw")
        channel_info = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel_info)
