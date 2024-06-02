from youtube_video_search import YouTubeVideoSearch
from youtube_follower_count import YouTubeFollowerCount

if __name__ == "__main__":
    search_query = "00:02:26"
    usernames = ["mrbeast", "tseries"]

    video_search = YouTubeVideoSearch()
    video_search.search_videos(search_query)

    print("-"*20, "\n")

    follower_count = YouTubeFollowerCount()
    follower_count.find_exact_number_of_followers(usernames)
