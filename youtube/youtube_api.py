import os
import re
import requests
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeAPI:
    API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    YOUTUBE_LINK = "https://www.youtube.com/watch?v="

    def __init__(self):
        self.api_key = self.verify_api_key()
        self.youtube = self.get_youtube_connection()

    def verify_api_key(self):
        if not self.API_KEY:
            print("No YOUTUBE_API_KEY variable found.")
            return input("Enter your YouTube Data API v3 key: ")
        return self.API_KEY

    def get_youtube_connection(self):
        try:
            youtube = build("youtube", "v3", developerKey=self.api_key)
            return youtube
        except HttpError as error:
            print(f"HTTP error: {error.resp.status}. API key is invalid or quota exceeded.")
        except Exception as error:
            print(f"Unexpected error: {error}")
        return None

