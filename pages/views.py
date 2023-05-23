from django.shortcuts import render
from script.youtube_api_crawling import youtube_api, youtube_comments


def index(request):
    return render(request, 'pages/index.html')


def filtering_youtube(request):
    return render(request, 'pages/filtering_youtube.html')


def process_input(request):
    if request.method == 'POST':
        input_value = request.POST.get('input_value')
        result = youtube_api(input_value)
        result_dict = dict(result)
        return render(request, 'pages/filtering_youtube.html', {'result_dict': result_dict})
    else:
        return render(request, 'pages/index.html')


def comments_view(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video_thumbnail = request.POST.get('video_thumbnail')
        video_title = request.POST.get('video_title')
        comments = youtube_comments(video_id)

        return render(request, 'pages/analysis_comment.html', {"comments": comments})
        # return render(request, 'pages/analysis_comment.html', {"comments": comments},
        #               {"thumbnail": video_thumbnail}, {"title": video_title})
    else:
        return render(request, 'pages/index.html')

