from django.contrib.auth.models import User, Group
from django.views import View
from rest_framework import viewsets
from .serializers import AASerializer, PostSerializer, ChartSerializer
from .models import AA, Post, Chart
from django.shortcuts import render,redirect
from rest_framework.response import Response
from .MySqlConn import MySqlConn
import pandas as pd
import folium
from folium.plugins import MarkerCluster, geocoder
import sys
from rest_framework.decorators import APIView
from folium import plugins
from collections import OrderedDict
from .fusioncharts import FusionCharts
import geocoder



sys.setrecursionlimit(10**7)




class AAViewSet(viewsets.ModelViewSet):
    queryset = AA.objects.all()
    serializer_class = AASerializer

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

    # g = geocoder.ip('me')
    @staticmethod
    def MapExe():
        df_select = map2.df_select
        map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=8)  # 시작위치 설정
        marker_cluster = MarkerCluster().add_to(map_osm)  # 군집화
        plugins.LocateControl().add_to(map_osm)

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
        return render(request, "main.html", {'map': maps,'a':a,'b':b,'c':c,'table':table})


def main(request):
    # g = geocoder.ip('me')
    # print(g.latlng)
    map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=9) #g.latlng [37.442803, 127.18161]
    plugins.LocateControl().add_to(map_osm)
    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    maps = map_osm._repr_html_()

    return render(request, 'main.html', {'map': maps})


class ChartAPIView(APIView):
    def get(self, request):
        serializer = ChartSerializer(Chart.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChartSerializer(data=request.data)
        dong = request.POST.get('dong')
        print(request.data.get("dong"))
        column3D = chart3D(dong)
        return render(request, 'chart.html', {'output': column3D.render()})  # render

def chart3D(dong):
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["data"] = []  # chartdata는 json형식이다.
    query1 = f"select male,female from seoul_ppl_dong where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query1)
    a = cursor.fetchone()

    # data 값 넣기
    dataSource["data"].append({"label": '남자', "value": a[0]})
    dataSource["data"].append({"label": '여자', "value": a[1]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = f"{dong}"
    chartConfig["subCaption"] = "남/녀 성비"
    chartConfig["xAxisName"] = "x축이름"
    chartConfig["yAxisName"] = "y축이름"
    chartConfig["numberSuffix"] = "명"  # y축 숫자단위
    chartConfig["theme"] = "fusion"  # 테마

    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    C3D = FusionCharts("pie3d", "myFirstChart", "600", "400", "chart-1", "json", dataSource)
    # 그래프 생성
    return C3D