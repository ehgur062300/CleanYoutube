# -*- coding: utf-8 -*-
"""youtubeAPI_crawling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gGfe7eQ-i9uslVmFh33ir9scQgQLdaJ1

# 최종본
"""

import pandas as pd
from googleapiclient.discovery import build


def file(target):
    found = False
    with open("static/filter.txt", encoding="utf-8") as f:
        for line in f:
            if target in line:
                found = True
                break

    if not found:
        with open("static/filter.txt", 'a', encoding='utf-8') as f:
            f.write(target.lower() + '\n')

def profile(youtuber):
    youtube = DEVELOPER_KEY()
    search_response = youtube.search().list(
        q=youtuber,
        order='relevance',
        part='snippet',
        maxResults=50
    ).execute()
    channel_id = search_response['items'][0]['id']['channelId']

    channels_response = youtube.channels().list(
        id=channel_id,
        part=['id', 'snippet', 'statistics', 'contentDetails']
    ).execute()
    #프로필 이름
    profile_name = channels_response['items'][0]['snippet']['title']
    #구독자 수
    subscriber = channels_response['items'][0]['statistics']['subscriberCount']
    #동영상 수
    video_count = channels_response['items'][0]['statistics']['videoCount']
    #대표 이미지
    profile_image = channels_response['items'][0]['snippet']['thumbnails']['medium']['url']

    profile_dict = {'profile_name': profile_name, 'subscriber': subscriber,
                    'video_count': video_count, 'profile_image': profile_image}
    transposed_profile_data = [profile_dict[key] for key in sorted(profile_dict)]
    profile_df = pd.DataFrame(transposed_profile_data)

    file(profile_name)

    return profile_df


def youtube_api(youtuber):
    youtube = DEVELOPER_KEY()
    search_response = youtube.search().list(
        q=youtuber,
        order='relevance',
        part='snippet',
        maxResults=50
    ).execute()

    channel_id = search_response['items'][0]['id']['channelId']

    channels_response = youtube.channels().list(
        id=channel_id,
        part=['id', 'snippet', 'statistics', 'contentDetails']
    ).execute()

    #-------메인부분---------
    #썸네일
    video_thumbnails_list = []
    #아이디
    video_ids_list = []
    #제목
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
                video_thumbnails_list.append(playlist_item["snippet"]["thumbnails"]["medium"]["url"])
                video_titles_list.append(playlist_item["snippet"]["title"])
                video_ids_list.append(playlist_item["snippet"]["resourceId"]["videoId"])

            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    pd_video_list_data = {"video_thumbnail": video_thumbnails_list,
                          "video_title": video_titles_list,
                          "video_id": video_ids_list}

    transposed_pd_video_list_data = [pd_video_list_data[key] for key in sorted(pd_video_list_data)]
    video_list_df = pd.DataFrame(transposed_pd_video_list_data)

    return video_list_df


def video_info(video_id):
    youtube = DEVELOPER_KEY()
    banner_video_request = youtube.videos().list(
        id=video_id,
        part=['id', 'snippet', 'statistics']
    ).execute()

    banner_videos_thumbnail = banner_video_request['items'][0]['snippet']['thumbnails']['medium']['url']
    banner_videos_title = banner_video_request['items'][0]['snippet']['title']
    banner_videos_viewcount = banner_video_request['items'][0]['statistics']['viewCount']
    banner_videos_likecount = banner_video_request['items'][0]['statistics']['likeCount']
    banner_videos_commentcount = banner_video_request['items'][0]['statistics']['commentCount']

    pd_banner_video_data = {'video_thumbnail': banner_videos_thumbnail, 'vdieo_title': banner_videos_title,
                            'video_viewcount': banner_videos_viewcount, 'vdieo_likecount': banner_videos_likecount,
                            'video_commentcount': banner_videos_commentcount}

    transposed_pd_banner_video_data = [pd_banner_video_data[key] for key in sorted(pd_banner_video_data)]
    video_info_df = pd.DataFrame(transposed_pd_banner_video_data)

    file(video_id)

    return video_info_df

def youtube_comments(video_id):
    comments = []
    youtube = DEVELOPER_KEY()
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

    comment_list = comment_df['comment'].tolist()
    new_list = []
    for x in comment_list:
        new_list.append(str(x))

    # 모든 댓글 내용을 하나의 문자열로 결합
    text = ' '.join(new_list)

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    with open("static/filter.txt", encoding="utf-8") as f:
        stopwords = set(f.read().splitlines())

    FONT_PATH = 'static/NanumGothic-Regular.ttf'

    # 워드 클라우드 생성
    wordcloud = WordCloud(font_path=FONT_PATH, width=800, height=800,
                          background_color='white', stopwords=stopwords, min_word_length=4).generate(text)

    # plt.figure(figsize=(8, 8), facecolor=None)
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.tight_layout(pad=0)

    # # 파일로 저장
    # plt.savefig('static/wordcloud.png')
    #
    # 단어의 빈도 계산
    wordcloud.generate_from_frequencies(wordcloud.process_text(text.lower()))
    word_freq = wordcloud.process_text(text.lower())

    word_freq.items()

    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    converted_dict = dict(sorted_word_freq)

    return comments, converted_dict
