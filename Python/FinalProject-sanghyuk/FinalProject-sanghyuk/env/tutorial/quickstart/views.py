from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.shortcuts import render, redirect
from .serializers import UserSerializer, GroupSerializer, AASerializer
from .models import AA
from .MySqlConn import MySqlConn
import pandas as pd
import folium
from folium.plugins import MarkerCluster

def index(request): #코드 구현
    return render(request, "index.html")

def ab(request):
        map = folium.Map(location=[37.553200102197415, 126.97119163543582], zoom_start=10, width='100%', height='80%', )
        maps = map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

        return render(request, "aa.html", {'map': maps})

def aa(request):

    class map2:
        df_select = None

        @staticmethod
        def MapMarker():
            cursor = MySqlConn.makeCursor()
            query = str.format("select m_name,m_lcn,m_lcc,lat,lng,m_mcn,m_mcc,m_scc from aa;")
            # cursor.execute(query)
            conn = MySqlConn.conn()
            df = pd.read_sql(query, conn)  # pandas로 읽기
            # print(df)
            df_lcc = df[df['m_lcc'] == 'Q']
            # mcc_series = df_lcc['m_mcc']
            # Map.MapMarker2(df_lcc , mcc_series)
            map2.df_select = df_lcc

            return df_lcc['m_mcc']
            # print(df_lcc)
            # Map.MapExe()

        @staticmethod
        def MapMarker2():
            # mcc = input('mcc 입력: ')
            df_lcc = map2.df_select
            df_mcc = df_lcc[df_lcc['m_mcc'] == 'Q08']
            map2.df_select = df_mcc

            return df_mcc['m_scc']
            # print(df_lcc)
            #map2.MapExe()

        @staticmethod
        def MapMarker3():  # 소분류 선택
            # scc = input('scc 입력: ')    ex) D16A01
            df_mcc = map2.df_select
            df_scc = df_mcc[df_mcc['m_scc'] == 'Q08A03']
            map2.df_select = df_scc

            # return df_mcc['m_scc']
            # print(df_lcc)
            map2.MapExe()

        @staticmethod
        def MapExe():
            df_select = map2.df_select
            #df1 = df[(df['m_lcc'] == 'D') & (df['m_mcc'] == 'D01')]     #pandas 조건문!
            # print(df1.isnull().sum())           #결측치확인
            map_osm = folium.Map(location=[36.5053542, 127.7043419], zoom_start=7)  # 시작위치 설정
            marker_cluster = MarkerCluster().add_to(map_osm)  # 군집화

            for i in df_select.index:  # for 문 사용 위도,경도로 위치 찍기  , # 행 우선 접근 방식으로 값 추출하기
                name = df_select.loc[i, 'm_name']
                lat = df_select.loc[i, 'lat']
                lng = df_select.loc[i, 'lng']

                # 추출한 정보를 지도에 표시
                marker = folium.Marker([lat, lng], popup=name)
                marker.add_to(marker_cluster)
            return map_osm


    map2.MapMarker()
    map2.MapMarker2()
    map2.MapMarker3()
    map_osm = map2.MapExe()
    maps = map_osm._repr_html_()

    return render(request, "aa.html", {'map': maps})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AAViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = AA.objects.all()
    serializer_class = AASerializer



