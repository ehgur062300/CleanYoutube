from django.shortcuts import render
from script.youtube_api_crawling import youtube_api, profile, video_info, youtube_comments

import pandas as pd


def index(request):
    return render(request, 'pages/index.html')


def process_input(request):
    if request.method == 'POST':
        input_value = request.POST.get('input_value')

        result_video = youtube_api(input_value)
        result_video_dict = dict(result_video)

        result_profile = profile(input_value)
        result_profile_dict = dict(result_profile)

        return render(request, 'pages/filtering_youtube.html', {'result_video_dict': result_video_dict,
                                                                'result_profile_dict': result_profile_dict})
    else:
        return render(request, 'pages/index.html')


def comments_view(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        comments, keyword = youtube_comments(video_id)

        comment_df = pd.DataFrame(comments)
        comment_df.columns = ['comment', 'author', 'date', 'like']
        comment_df.to_excel('script/comments.xlsx', index=False)

        video_info_data = video_info(video_id)
        video_info_data.to_excel('script/video_info.xlsx', index=False)

        return render(request, 'pages/analysis_comment.html', {"comments": comments,
                                                               "video_info": dict(video_info_data),
                                                               "video_id": video_id,
                                                               "keyword": keyword
                                                               })
    else:
        return render(request, 'pages/index.html')


def bad_comments_view(request):
    comment_data = pd.read_excel('script/comments2.xlsx')
    comments = comment_data.values.tolist()

    video_data = pd.read_excel('script/video_info.xlsx')
    video_data_list = video_data.transpose().values.tolist()

    return render(request, 'pages/analysis_bad_comment.html', {"comments": comments,
                                                               "video_info": video_data_list,
                                                               })
