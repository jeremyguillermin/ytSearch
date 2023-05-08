from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import youtube_dl
import argparse
import os
import re


api_key = "api_key"
youtube = build("youtube", "v3", developerKey=api_key)

def search_videos(query, language, max_results=10, sort_by="relevance", published_after=None, published_before=None):
    try:
        search_response = youtube.search().list(
            q=query,
            type="video",
            videoCaption="closedCaption",
            relevanceLanguage=language,
            maxResults=max_results,
            order=sort_by,
            publishedAfter=published_after,
            publishedBefore=published_before,
            part="id,snippet"
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

    return search_response.get("items", [])

def search_videos_in_channel(channel_id, query, language, max_results=10, sort_by="relevance", published_after=None, published_before=None):
    try:
        search_response = youtube.search().list(
            q=query,
            type="video",
            videoCaption="closedCaption",
            relevanceLanguage=language,
            channelId=channel_id,
            maxResults=max_results,
            order=sort_by,
            publishedAfter=published_after,
            publishedBefore=published_before,
            part="id,snippet"
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

    return search_response.get("items", [])

def get_video_transcripts(video_id, language):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language])
        return transcript.fetch()
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def search_keywords_in_transcript(transcript, keywords, context_range=2, use_regex=False):
    results = []
    for i, entry in enumerate(transcript):
        if use_regex:
            if any(re.search(keyword.lower(), entry["text"].lower()) for keyword in keywords):
                start_index = max(0, i - context_range)
                end_index = min(len(transcript), i + context_range + 1)
                results.append(transcript[start_index:end_index])
        else:
            if any(keyword.lower() in entry["text"].lower() for keyword in keywords):
                start_index = max(0, i - context_range)
                end_index = min(len(transcript), i + context_range + 1)
                results.append(transcript[start_index:end_index])
    return results

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes}:{seconds:02d}"

def highlight_keywords(text, keywords, use_regex=False):
    if use_regex:
        for keyword in keywords:
            text = re.sub(f'({keyword})', r'\033[1;31m\1\033[0m', text, flags=re.IGNORECASE)
    else:
        for keyword in keywords:
            text = re.sub(f'({re.escape(keyword)})', r'\033[1;31m\1\033[0m', text, flags=re.IGNORECASE)

    return text

def get_channel_id(channel_name):
    try:
        search_response = youtube.search().list(
            q=channel_name,
            type="channel",
            maxResults=1,
            part="id"
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

    if search_response.get("items"):
        return search_response["items"][0]["id"]["channelId"]
    else:
        return None

def main(query, keywords, language, max_results, channel_id=None, sort_by="relevance", published_after=None, published_before=None, use_regex=False):
    if channel_id:
        videos = search_videos_in_channel(channel_id, query, language, max_results, sort_by, published_after, published_before)
    else:
        videos = search_videos(query, language, max_results, sort_by, published_after, published_before)

    for video in videos:
        video_id = video["id"]["videoId"]
        video_title = video["snippet"]["title"]
        channel_title = video["snippet"]["channelTitle"]
        transcript = get_video_transcripts(video_id, language)

        if transcript:
            matched_contexts = search_keywords_in_transcript(transcript, keywords, use_regex=use_regex)

            if matched_contexts:
                publish_date_str = video["snippet"]["publishedAt"]
                publish_date = datetime.strptime(publish_date_str, "%Y-%m-%dT%H:%M:%SZ")
                publish_date_str = publish_date.strftime("%d/%m/%Y")
                
                print(f"\n\033[1;34mVideo:\033[0m {video_title}")
                print(f"\033[1;34mChaîne:\033[0m {channel_title}")
                print(f"\033[1;34mDate de sortie:\033[0m {publish_date_str}\n")

                for context in matched_contexts:
                    start_time = format_time(context[0]['start'])
                    end_time = format_time(context[-1]['start'])
                    text = ' '.join(entry['text'] for entry in context)
                    highlighted_text = highlight_keywords(text, keywords, use_regex=use_regex)
                    
                    print(f"\033[1;33mExtrait ({start_time} / {end_time}): \033[0m")
                    print(highlighted_text)

                    print(f"\n\033[1;32mURL:\033[0m https://www.youtube.com/watch?v={video_id}&t={context[0]['start']}s")
                    print("\n" + "-" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Search query for YouTube videos (optional)")
    parser.add_argument("--keywords", "-k", nargs="*", help="Keywords to search in transcripts (optional, can be multiple)")
    parser.add_argument("--language", "-l", default="en", help="Language code for transcripts (default: en)")
    parser.add_argument("--max-results", "-m", type=int, default=10, help="Max number of search results (default: 10)")
    parser.add_argument("--channel-id", "-c", help="Search videos in a specific YouTube channel (optional)")
    parser.add_argument("--search-channel", "-s", help="Search for a YouTube channel ID by channel name (optional)")
    parser.add_argument("--sort-by", "-d", choices=["date", "rating", "relevance", "title", "videoCount", "viewCount"], default="relevance", help="Sort search results by (default: relevance)")
    parser.add_argument("--published-after", "-a", help="Search videos published after a specific date (format: YYYY-MM-DD)")
    parser.add_argument("--published-before", "-b", help="Search videos published before a specific date (format: YYYY-MM-DD)")
    parser.add_argument("--use-regex", "-r", action="store_true", help="Use regular expressions for keyword matching (default: False)")

    args = parser.parse_args()

    if args.search_channel:
        channel_id = get_channel_id(args.search_channel)
        if channel_id:
            print(f"Channel ID for '{args.search_channel}': {channel_id}")
        else:
            print(f"No channel found with the name '{args.search_channel}'")
    else:
        main(args.query, args.keywords, args.language, args.max_results, args.channel_id, args.sort_by, args.published_after, args.published_before, args.use_regex)