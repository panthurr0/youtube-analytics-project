import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.__youtube = self.get_service()
        self.__playlist_id = playlist_id
        self.pl_videos = self.__youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                             part="contentDetails,snippet",
                                                             maxResults=50,
                                                             ).execute()
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"
        self.video_ids = [video['contentDetails']['videoId'] for video in self.pl_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.video_ids)
                                                               ).execute()
        self.channel_id = self.pl_videos['items'][0]['snippet']['channelId']
        self.title = self.get_title(self.channel_id, self.__playlist_id, self.__youtube)

    @property
    def total_duration(self):
        """
        :return: Общее время плейлиста
        """
        duration_list = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))

    @property
    def playlist_id(self):
        return self.__playlist_id

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @staticmethod
    def get_title(channel_id, playlist_id, youtube):
        """
        :return: Название плейлиста
        """
        playlists = youtube.playlists().list(channelId=channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                title = playlist['snippet']['title']
                return title

    def show_best_video(self):
        """
        :return: Ссылка на видеоролик, имеющий самое большое количество лайков в плейлисте
        """
        youtube = self.get_service()

        video_response: list = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=','.join(self.video_ids)
                                                     ).execute()
        max_likes: int = 0

        best_video_id: str = ''

        for info in video_response['items']:
            if int(info['statistics']['likeCount']) > max_likes:
                max_likes: int = int(info['statistics']['likeCount'])
                best_video_id: str = info['id']

        return f"https://youtu.be/{best_video_id}"
