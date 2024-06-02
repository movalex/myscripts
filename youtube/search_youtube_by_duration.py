import re
import os
import time
import requests
import googleapiclient.discovery
from datetime import timedelta
from functools import reduce

API_TEST_CHANNEL = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers YouTube channel
API_KEY = os.getenv("YOUTUBE_API_KEY", "")

MAX_RESULTS = 20
DEBUG = False
YOUTUBE_LINK = "https://www.youtube.com/watch?v="


def get_youtube_connection(api_key):
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
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


def get_video_duration_timedelta(youtube, video_id) -> timedelta:
    try:
        video_response = (
            youtube.videos().list(part="contentDetails", id=video_id).execute()
        )
        duration_iso = video_response["items"][0]["contentDetails"]["duration"]
        print(duration_iso)
        duration_timedelta = youtube_duration_iso_to_timedelta(duration_iso)

        return duration_timedelta
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP Error occurred: {e}")
        return None
    except KeyError:
        print("Unexpected response format.")
        return None


def categorize_video_duration(duration: timedelta, thresholds=(4, 20)) -> str:
    """
    Categorizes a video duration as 'short', 'medium', or 'long'.
    """
    total_minutes = duration.total_seconds() / 60
    if total_minutes < thresholds[0]:
        return "short"
    elif total_minutes < thresholds[1]:
        return "medium"
    else:
        return "long"


def process_response(
    youtube, search_response, target_video_duration, tolerance_seconds=3
):
    results = {}
    for element in search_response.get("items", []):
        video_id = element["id"]["videoId"]
        video_duration = get_video_duration_timedelta(youtube, video_id)

        # Calculate the tolerance window
        lower_bound = target_video_duration - timedelta(seconds=tolerance_seconds)
        upper_bound = target_video_duration + timedelta(seconds=tolerance_seconds)

        if video_duration and lower_bound <= video_duration <= upper_bound:
            video_title = element["snippet"]["title"]
            link = f"{YOUTUBE_LINK}{video_id}"
            results[link] = video_duration
    if not results:
        print(
            f"No videos found within {tolerance_seconds} seconds tolerance of for {MAX_RESULTS} searched videos\n"
        )
    else:
        print(
            f"Links within {tolerance_seconds} seconds tolerance for {MAX_RESULTS} searched videos\n"
        )
        for link, duration in results.items():
            print(f"{link} - ({duration})")
        print(f"\nTotal links found: {len(results)}")


def verify_api_key():
    api_key = API_KEY
    if API_KEY == "":
        print("No YOUTUBE_API_KEY variable found.")
        api_key = input("Enter your YouTube Data API v3 key: ")
    return api_key


def get_channel_id(user_name: str, api_key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={user_name}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    channel_id = data["items"][0]["id"]
    return channel_id


def find_exact_number_of_followers(username_list):
    api_key = verify_api_key()
    results = {}

    for username in username_list:
        channel_id = get_channel_id(username, api_key)
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        subscriber_count = data["items"][0]["statistics"]["subscriberCount"]
        print(f"{username}'s subscriber Count: {subscriber_count}")
        results[username] = subscriber_count

    value1, value2 = results.values()
    difference = abs(int(value2) - int(value1))
    print(f"The difference in subsribers number: {difference}")


def search_youtube_videos(search_query):
    api_key = verify_api_key()

    youtube = get_youtube_connection(api_key)
    if not youtube:
        return

    # Categorize YouTube video duration

    target_video_duration = duration_to_timedelta(search_query)
    target_video_duration_type = categorize_video_duration(target_video_duration)
    print(f"Searching for {target_video_duration_type} videos...\n")

    search_response = (
        youtube.search()
        .list(
            q=search_query,
            part="id,snippet",
            type="video",
            videoDuration=target_video_duration_type,
            maxResults=MAX_RESULTS,
        )
        .execute()
    )
    process_response(youtube, search_response, target_video_duration)


def youtube_duration_iso_to_timedelta(duration) -> timedelta:
    # Regular expression to find hours, minutes, and seconds
    pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
    match = pattern.match(duration)

    if not match:
        return None  # Return None if the pattern does not match

    # Extract hours, minutes, and seconds from the match, defaulting to 0 if not found
    hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def duration_to_timedelta(duration: str) -> timedelta:
    h, m, s = [int(i) for i in duration.split(":")]
    return timedelta(hours=h, minutes=m, seconds=s)


if __name__ == "__main__":
    search_query = "00:03:26"

    # search_youtube_videos(search_query)
    find_exact_number_of_followers(["mrbeast", "alexybogomolov"])
