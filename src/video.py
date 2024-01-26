import os

from googleapiclient.discovery import build


class Video():
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        """
        video_title:
        view_count:
        like_count:
        comment_count:
        """
        self.__video_id = video_id
        self.share_attributes()

    def share_attributes(self):
        response = self.video_response()
        self.video_title: str = response['items'][0]['snippet']['title']
        self.view_count: int = response['items'][0]['statistics']['viewCount']
        self.like_count: int = response['items'][0]['statistics']['likeCount']
        self.comment_count: int = response['items'][0]['statistics']['commentCount']
        self.url = f"https://www.youtube.com/channel/{self.video_id}"

    def __str__(self):
        return f'{self.video_title}'

    @property
    def video_id(self):
        return self.__video_id

    @classmethod
    def get_service(cls):
        """
        :return: Объект, для работы с YT API.
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    def video_response(self):
        youtube = self.get_service()
        return youtube.videos().list(id=self.__video_id, part="snippet,contentDetails,statistics").execute()


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        super().share_attributes()
        self.share_attributes()
        self.url = f"https://www.youtube.com/watch?v={self.video_id}&list={self.playlist_id}"
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
