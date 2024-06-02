import re
from youtube_api import YouTubeAPI
from datetime import timedelta
from googleapiclient.errors import HttpError


class YouTubeVideoSearch(YouTubeAPI):
    MAX_RESULTS = 20

    def youtube_duration_iso_to_timedelta(self, duration) -> timedelta:
        pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
        match = pattern.match(duration)
        if not match:
            return None
        hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def duration_to_timedelta(self, duration: str) -> timedelta:
        h, m, s = map(int, duration.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def get_video_duration_timedelta(self, video_id):
        try:
            video_response = (
                self.youtube.videos().list(part="contentDetails", id=video_id).execute()
            )
            duration_iso = video_response["items"][0]["contentDetails"]["duration"]
            return self.youtube_duration_iso_to_timedelta(duration_iso)
        except HttpError as error:
            print(f"HTTP error: {error}")
        except KeyError:
            print("Unexpected response format.")
        return None

    def categorize_video_duration(self, duration, thresholds=(4, 20)):
        total_minutes = duration.total_seconds() / 60
        if total_minutes < thresholds[0]:
            return "short"
        elif total_minutes < thresholds[1]:
            return "medium"
        else:
            return "long"

    def process_response(
        self, search_response, target_video_duration, tolerance_seconds=3
    ):
        results = {}
        lower_bound = target_video_duration - timedelta(seconds=tolerance_seconds)
        upper_bound = target_video_duration + timedelta(seconds=tolerance_seconds)

        for element in search_response.get("items", []):
            video_id = element["id"]["videoId"]
            video_duration = self.get_video_duration_timedelta(video_id)
            if video_duration and lower_bound <= video_duration <= upper_bound:
                video_title = element["snippet"]["title"]
                link = f"{self.YOUTUBE_LINK}{video_id}"
                results[link] = video_duration

        self.print_results(results, tolerance_seconds)

    def print_results(self, results, tolerance_seconds):
        if not results:
            print(
                f"No videos found within {tolerance_seconds} seconds tolerance for {self.MAX_RESULTS} searched videos\n"
            )
        else:
            print(
                f"Links within {tolerance_seconds} seconds tolerance for {self.MAX_RESULTS} searched videos\n"
            )
            for link, duration in results.items():
                print(f"{link} - ({duration})")
            print(f"\nTotal links found: {len(results)}")

    def search_videos(self, search_query):
        target_video_duration = self.duration_to_timedelta(search_query)
        target_video_duration_type = self.categorize_video_duration(
            target_video_duration
        )
        print(f"Searching for {target_video_duration_type} videos...\n")

        search_response = (
            self.youtube.search()
            .list(
                q=search_query,
                part="id,snippet",
                type="video",
                videoDuration=target_video_duration_type,
                maxResults=self.MAX_RESULTS,
            )
            .execute()
        )
        self.process_response(search_response, target_video_duration)
