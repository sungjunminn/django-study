from django.contrib.auth.models import User, Group
from django.views import View
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, AASerializer, PostSerializer, ChartSerializer
from .models import AA, Post, Chart
from django.shortcuts import render,redirect
from rest_framework.response import Response
from .MySqlConn import MySqlConn
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import sys
from rest_framework.decorators import APIView
from folium import plugins
from collections import OrderedDict
from .fusioncharts import FusionCharts
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
        return render(request, "map.html", {'map': maps,'a':a,'b':b,'c':c,'table':table})

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

def test(request):
    map_osm = folium.Map(location=[36.142803, 128.18161], zoom_start=7)
    maps = map_osm._repr_html_()
    return render(request, 'test.html', {'map': maps})

def dash(request):
    # pie_chart_ppl = []
    #
    # all_sum = SeoulPplDong.all_sum.filter(dong="사직동")
    # man_ppl = SeoulPplDong.male.filter(dong="사직동")
    # female_ppl = SeoulPplDong.female.filter(dong="사직동")
    # pie_chart_ppl = [man_ppl, female_ppl]
    return render(request, 'dashboard.html')

def dashmap(request):
    map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=9)
    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    maps = map_osm._repr_html_()
    return render(request, 'map.html', {'map': maps})

def dashmap2(request):
    map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=9)
    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    maps = map_osm._repr_html_()
    return render(request, 'map2.html', {'map': maps})


class chart_VIEW(View):
    def get(self, request):
        # chartdata 선언
        dataSource = OrderedDict()
        dataSource["data"] = []  # chartdata는 json형식이다.

        # data 값 넣기
        dataSource["data"].append({"label": 'data1', "value": '290'})
        dataSource["data"].append({"label": 'data2', "value": '50'})
        dataSource["data"].append({"label": 'data3', "value": '180'})
        dataSource["data"].append({"label": 'data4', "value": '140'})
        dataSource["data"].append({"label": 'data5', "value": '100'})
        dataSource["data"].append({"label": 'data6', "value": '115'})

        chartConfig = OrderedDict()
        chartConfig["caption"] = "제목"
        chartConfig["subCaption"] = "소제목"
        chartConfig["xAxisName"] = "x축이름"
        chartConfig["yAxisName"] = "y축이름"
        chartConfig["numberSuffix"] = "K"  # y축 숫자단위
        chartConfig["theme"] = "fusion"  # 테마

        # 그래프 특징 설정
        dataSource["chart"] = chartConfig

        column2D = FusionCharts("column2d", "myFirstChart", "500", "400", "chart-1", "json", dataSource)
        # 그래프 생성

        return render(request, 'dashboard.html', {'output': column2D.render()})  # render

class ChartAPIView(APIView):
    def get(self, request):
        serializer = ChartSerializer(Chart.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChartSerializer(data=request.data)
        dong = request.POST.get('dong')
        print(request.data.get("dong"))
        column3D = chart3D(dong)
        return render(request, 'dashboard.html', {'output': column3D.render()})  # render

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