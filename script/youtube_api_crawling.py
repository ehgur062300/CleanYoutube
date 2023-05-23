from googleapiclient.discovery import build
import pandas as pd


def youtube_api(youtuber):
    DEVELOPER_KEY = 'AIzaSyA_9qUEVsYKlQdziqj1wxg8MU2ETt0Uizk'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # 채널 id 가져오기
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=youtuber,
        order='relevance',
        part='snippet',
        maxResults=50
    ).execute()

    channel_id = search_response['items'][0]['id']['channelId']

    channels_response = youtube.channels().list(
        id=channel_id,
        part="contentDetails"
    ).execute()

    video_thumbnails_list = []
    video_ids_list = []
    video_titles_list = []
    for channel in channels_response["items"]:
        uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part="snippet",
            maxResults=50
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Insert information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                video_thumbnails_list.append(playlist_item["snippet"]["thumbnails"]["default"]["url"])
                video_titles_list.append(playlist_item["snippet"]["title"])
                video_ids_list.append(playlist_item["snippet"]["resourceId"]["videoId"])

            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    pd_data = {"video_thumbnail": video_thumbnails_list, "video_title": video_titles_list, "video_id": video_ids_list}
    transposed_pd_data = [pd_data[key] for key in sorted(pd_data)]
    video_df = pd.DataFrame(transposed_pd_data)

    return video_df


def youtube_comments(video_id):
    comments = []
    DEVELOPER_KEY = 'AIzaSyA_9qUEVsYKlQdziqj1wxg8MU2ETt0Uizk'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # 채널 id 가져오기
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    comment_list_response = youtube.commentThreads().list(
        videoId=video_id,
        order='relevance',
        part='snippet,replies',
        maxResults=100
    ).execute()

    while comment_list_response:
        for item in comment_list_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']

            comments.append([comment['textDisplay'], comment['authorDisplayName'],
                             comment['publishedAt'], comment['likeCount']])
        if item['snippet']['totalReplyCount'] > 0:
            for reply_item in item['replies']['comments']:
                reply = reply_item['snippet']
                comments.append([reply['textDisplay'], reply['authorDisplayName'],
                                 reply['publishedAt'], reply['likeCount']])

        if 'nextPageToken' in comment_list_response:
            comment_list_response = youtube.commentThreads().list(
                videoId=video_id,
                order='relevance',
                part='snippet,replies',
                pageToken=comment_list_response['nextPageToken'],
                maxResults=100
            ).execute()

        else:
            break

    comment_df = pd.DataFrame(comments)
    comment_df.columns = ['comment', 'author', 'date', 'like']
    return comments
