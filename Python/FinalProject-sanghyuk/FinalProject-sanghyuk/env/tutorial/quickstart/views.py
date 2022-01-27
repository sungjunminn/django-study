from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, AASerializer, PostSerializer
from .models import AA, Post
from django.shortcuts import render,redirect
from rest_framework.response import Response
from .MySqlConn import MySqlConn
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import sys
from rest_framework.decorators import APIView
import json
from django.http import HttpResponse, JsonResponse,request
sys.setrecursionlimit(10**7)


def index(request): #코드 구현
    return render(request, "index.html")


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
    queryset = AA.objects.all()
    serializer_class = AASerializer

# class AAView(api_view):
#
#     def get(self, request):
#         filter_categories ={
#             'm_lcc': 'detail_m_scc__sub_m_cc__m_lcc__in',
#             'm_mcc': 'detail_m_scc__sub_m_cc__in',
#             'm_scc': 'detail_m_scc__in'
#         }
#
#         filter_set = {
#             filter_categories.get(key): value for (key, value) in dict(request.GET).items()
#             if filter_categories.get(key)
#         }
#         return AA.objects.filter(**filter_set).distinct()

def home(request) :
    map = folium.Map(location=[37.7854, 128.4698],zoom_start=15, width='100%', height='100%',)
    maps=map._repr_html_() #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환
    return render(request,'../templates/home.html',{'map' : maps})


# # @APIView(['GET'])
# def show():
#     if request.method == 'GET':
#         a = request.json["a"]
#         b = request.json["b"]
#         c = request.json["c"]
#         d = MapMarker(a,b,c)
#     return d
# def aa(request):
#
#     class map2:
#         df_select = None
#
#
#         @staticmethod
#         def MapMarker(a):
#
#             cursor = MySqlConn.makeCursor()
#             query = str.format("select m_name,m_lcn,m_lcc,lat,lng,m_mcn,m_mcc,m_scc from aa;")
#             conn = MySqlConn.conn()
#             df = pd.read_sql(query, conn)  # pandas로 읽기
#             df_lcc = df[df['m_lcc'] == a]
#             map2.df_select = df_lcc
#             return df_lcc['m_mcc']
#
#         @staticmethod
#         def MapMarker2(b):
#
#             df_lcc = map2.df_select
#             df_mcc = df_lcc[df_lcc['m_mcc'] == b]
#             map2.df_select = df_mcc
#             return df_mcc['m_scc']
#
#         @staticmethod
#         def MapMarker3(c):  # 소분류 선택
#
#             df_mcc = map2.df_select
#             df_scc = df_mcc[df_mcc['m_scc'] == c]
#             map2.df_select = df_scc
#             map2.MapExe()
#
#         @staticmethod
#         def MapExe():
#             df_select = map2.df_select
#             map_osm = folium.Map(location=[36.5053542, 127.7043419], zoom_start=7)  # 시작위치 설정
#             marker_cluster = MarkerCluster().add_to(map_osm)  # 군집화
#
#             for i in df_select.index:  # for 문 사용 위도,경도로 위치 찍기  , # 행 우선 접근 방식으로 값 추출하기
#                 name = df_select.loc[i, 'm_name']
#                 lat = df_select.loc[i, 'lat']
#                 lng = df_select.loc[i, 'lng']
#
#                 # 추출한 정보를 지도에 표시
#                 marker = folium.Marker([lat, lng], popup=name)
#                 marker.add_to(marker_cluster)
#             return map_osm
#
#     a = request.json["m_lcc"]
#     b = request.json["m_mcc"]
#     c = request.json["m_scc"]
#     map2.MapMarker(a)
#     map2.MapMarker2(b)
#     map2.MapMarker3(c)
#     map_osm = map2.MapExe()
#     maps = map_osm._repr_html_()
#
#     return render(request, "aa.html", {'map': maps})

class map2:
    df_select = None


    @staticmethod
    def MapMarker(a,table):

        cursor = MySqlConn.makeCursor()
        # query = str.format("select m_name,m_lcn,m_lcc,lat,lng,m_mcn,m_mcc,m_scc,m_scn from aa;")
        query = f"select m_name,m_lcn,lat,lng,m_mcn,m_scn from {table};"
        conn = MySqlConn.conn()
        df = pd.read_sql(query, conn)  # pandas로 읽기
        df_lcn = df[df['m_lcn'] == a]
        map2.df_select = df_lcn
        return df_lcn['m_mcn']

    @staticmethod
    def MapMarker2(b):

        df_lcn = map2.df_select
        df_mcn = df_lcn[df_lcn['m_mcn'] == b]
        map2.df_select = df_mcn
        return df_mcn['m_scn']

    @staticmethod
    def MapMarker3(c):  # 소분류 선택

        df_mcn = map2.df_select
        df_scn = df_mcn[df_mcn['m_scn'] == c]
        map2.df_select = df_scn
        map2.MapExe()

    @staticmethod
    def MapExe():
        df_select = map2.df_select
        map_osm = folium.Map(location=[36.142803, 128.18161], zoom_start=8)  # 시작위치 설정
        marker_cluster = MarkerCluster().add_to(map_osm)  # 군집화

        for i in df_select.index:  # for 문 사용 위도,경도로 위치 찍기  , # 행 우선 접근 방식으로 값 추출하기
            name = df_select.loc[i, 'm_name']
            lat = df_select.loc[i, 'lat']
            lng = df_select.loc[i, 'lng']

            # 추출한 정보를 지도에 표시
            marker = folium.Marker([lat, lng], popup=name)
            marker.add_to(marker_cluster)
        return map_osm






class PostAPIView(APIView):
    def get(self,request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)
        # serializer = PostSerializer(data=request.data)
        table = request.data.get("table")
        a = request.data.get("m_lcc")
        b = request.data.get("m_mcc")
        c = request.data.get("m_scc")
        print(request.data.get("table"))
        print(request.data.get("m_lcc"))
        print(request.data.get("m_mcc"))
        print(request.data.get("m_scc"))
        map2.MapMarker(a,table)
        map2.MapMarker2(b)
        map2.MapMarker3(c)
        map_osm = map2.MapExe()
        maps = map_osm._repr_html_()
        # return Response(serializer.errors)
        return render(request, "post.html", {'map': maps})

from django.shortcuts import get_object_or_404

# class PostDetailAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Post, pk=pk)
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

def asdf(request):
    return render(request, 'aa.html')

def qwer(request):
    map_osm = folium.Map(location=[36.142803, 128.18161], zoom_start=7)
    maps = map_osm._repr_html_()
    return render(request, 'qwer.html', {'map': maps})

def abc(request):
    map_osm = folium.Map(location=[36.142803, 128.18161], zoom_start=7)
    maps = map_osm._repr_html_()
    return render(request, 'datamaps.html', {'map': maps})
