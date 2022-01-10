from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from folium import plugins
from folium.plugins import MarkerCluster
import folium
import geocoder
from .models import Question
from django.utils import timezone
import json
import pandas as pd
import urllib.request
import datetime
import time
import webbrowser
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

g = geocoder.ip('me') #나의 현재위치

def mapbase(request):  #지도
    map = folium.Map(location=g.latlng,zoom_start=15, width='100%', height='100%',)
    with open('templates/pybo/seoul_municipalities_geo.json', mode='rt', encoding='utf-8') as f: #서울시행정구역json파일로 구역설정
        geo = json.loads(f.read())
        f.close()
    folium.GeoJson(geo, name='seoul_municipalities').add_to(map)                                 #seoul_municipalities.html파일을 map에 업로드
    map.save('mapbase.html')
    #folium.CircleMarker([37.566345, 126.977893],radius=10, fill_color='#3186cc').add_to(map)       #지도 위에 마커 생성

    plugins.LocateControl().add_to(map)
    plugins.Geocoder().add_to(map)

    maps=map._repr_html_()

    return render(request, 'pybo/mapbase.html',{'map' : maps}) #pybo안의 mapbase.html(행정구역)파일 경로





def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)







