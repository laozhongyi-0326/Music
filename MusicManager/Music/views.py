from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Music.crawler_spider_helper import get_music_list
# Create your views here.

def music_list(request):
    if request.method == 'GET':
        key_word = request.GET.get('key_word')
        music_item_list = get_music_list(key_word)
        lenes = len(music_item_list)
        content = {'music_item_list': music_item_list, 'lists': range(lenes+1)}

    return render(request, 'music_html/music_list.html', content)


