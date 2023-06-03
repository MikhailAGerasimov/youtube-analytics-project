import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_list = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channelid = self.channel_list["items"][0]["id"]
        self.title = self.channel_list["items"][0]["snippet"]["title"]
        self.video_count = self.channel_list["items"][0]["statistics"]["videoCount"]
        self.url = "https://www.youtube.com/channel/" + self.__channelid
        self. subscriber_count = self.channel_list["items"][0]["statistics"]["subscriberCount"]
        self.view_count = self.channel_list["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channelid

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_list, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API вне класса"""
        return cls.youtube

    def to_json(self, filename):
        """Записывает аттрибуты класса в json файл"""
        with open(filename, 'w') as outfile:
            json.dump(self.__dict__, outfile)
