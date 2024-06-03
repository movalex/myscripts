import os
import re
import requests
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeAPI:
    API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    API_TEST_CHANNEL = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers YouTube channel
    YOUTUBE_LINK = "https://www.youtube.com/watch?v="

    def __init__(self):
        self.api_key = self.verify_api_key()
        self.youtube = self.get_youtube_connection()

    def get_youtube_connection(self, api_key):
        try:
            youtube = googleapiclient.discovery.build(
                "youtube", "v3", developerKey=api_key
            )
            if not DEBUG:
                return youtube

            # Use the 'channels.list' method to make a test request. This uses a well-known channel ID.
            request = youtube.channels().list(part="id", id=API_TEST_CHANNEL)
            response = request.execute()

            if response and response.get("items"):
                print("API key is valid.")
                return youtube
            else:
                print("API key is valid but check the response for expected data.")
                return False
        except googleapiclient.errors.HttpError as error:
            if error.resp.status in [403, 400]:
                print("API key is invalid or quota exceeded.")
            else:
                print(f"An unexpected HTTP error occurred: {error.resp.status}")
            return False
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            return False

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
            print(
                f"HTTP error: {error.resp.status}. API key is invalid or quota exceeded."
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
        return None
