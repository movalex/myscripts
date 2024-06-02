import requests
from youtube_api import YouTubeAPI

class YouTubeFollowerCount(YouTubeAPI):

    def get_channel_id(self, user_name):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={user_name}&key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["items"][0]["id"]

    def get_subscriber_count(self, channel_id):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["items"][0]["statistics"]["subscriberCount"]

    def find_exact_number_of_followers(self, username_list):
        results = {username: self.get_subscriber_count(self.get_channel_id(username)) for username in username_list}
        self.print_subscriber_counts(results)

    def print_subscriber_counts(self, results):
        for username, count in results.items():
            print(f"{username}'s subscriber Count: {count}")
        diff = abs(int(list(results.values())[1]) - int(list(results.values())[0]))
        print(f"The difference in subscribers number: {diff}")
