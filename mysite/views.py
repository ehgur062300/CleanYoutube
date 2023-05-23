from django.shortcuts import render
from .models import PositiveWords, NegativeWords


def positive(request):
    positive_word_list = PositiveWords.objects.order_by()
    positive_context = {'positive_word_list': positive_word_list}

    return render(request, 'mysite/positive_word_list.html', positive_context)


def negative(request):
    negative_word_list = NegativeWords.objects.order_by()
    negative_context = {'negative_word_list': negative_word_list}

    return render(request, 'mysite/negative_word_list.html', negative_context)
