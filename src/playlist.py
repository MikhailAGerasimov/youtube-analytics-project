from googleapiclient.discovery import build
import os
import datetime
import isodate

class PlayList():
    """Класс для плей-листа"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, pl_id):
        """Экземпляр инициализируется id плей-листа. Дальше все данные будут подтягиваться по API."""
        self.pl_response = self.youtube.playlists().list(part='snippet', id=pl_id).execute()
        self.pl_id = self.pl_response["items"][0]["id"]
        self.title = self.pl_response["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + self.pl_id

    @property
    def total_duration(self):
        """
        Метод возварщает длительность всех видеоролико плей-листа
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_duration: datetime
        total_duration = 0
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration).total_seconds()
            total_duration += duration
        return datetime.timedelta(seconds=float(total_duration))


    def show_best_video(self):
        """
        Метод, возвращающий ссылку на видео с наибельшим числом лайков
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        current_likes = 0
        best_url = ''
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > current_likes:
                 best_url = 'https://youtu.be/' + video['id']
        return best_url

