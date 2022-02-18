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
        return render(request, "index.html", {'map': maps,'a':a,'b':b,'c':c,'table':table})


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
        column2D = line_population_live(dong)
        mscolumn2d = age_population(dong)
        g_point = grade(dong)
        total_p = text(dong)
        sede = chartmin1(dong)
        jutaek = chartjD(dong)
        choi = chart3D_Job(dong)
        # park_grade = score_G(dong)
        return render(request, 'chart.html',
                      {'output': column3D.render(), 'output2': column2D.render(), 'output3': mscolumn2d.render(),
                       'apt_u': g_point['apt_u'], 'apt_grade': g_point['apt_grade'], 'apt_dong': g_point['apt_dong'],
                       'score': g_point['score'], 'total_p': total_p,
                       'output4': sede.render(), 'output5': jutaek.render(), 'output6': choi.render()})  # rende

def chart3D(dong): #남녀성비 파이그래프
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
    chartConfig["caption"] = "남/녀 성비"
    # chartConfig["subCaption"] = "남/녀 성비"
    chartConfig["xAxisName"] = "x축이름"
    chartConfig["yAxisName"] = "y축이름"
    chartConfig["numberSuffix"] = "명"  # y축 숫자단위
    chartConfig["theme"] = "fusion"  # 테마
    chartConfig["bgcolor"] = '#f8f8ff'

    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    C3D = FusionCharts("pie2d", "myFirstChart", "450", "350", "chart-1", "json", dataSource)
    # 그래프 생성
    return C3D


def chart3D_Job(dong):  #직장인 남/녀 성비
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["data"] = []  # chartdata는 json형식이다.
    query1 = f"select male,female from dong_job_ppt where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query1)
    a = cursor.fetchone()

    # data 값 넣기
    dataSource["data"].append({"label": '남자', "value": a[0]})
    dataSource["data"].append({"label": '여자', "value": a[1]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = "직장인 남/녀 성비"
    chartConfig["xAxisName"] = "x축이름"
    chartConfig["yAxisName"] = "y축이름"
    chartConfig["numberSuffix"] = "명"  # y축 숫자단위
    chartConfig["bgcolor"] = '#f8f8ff'
    chartConfig["theme"] = "fusion"  # 테마


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    C3D_Job = FusionCharts("column2d", "choiChart2", "450", "350", "choi-2", "json", dataSource)
    # 그래프 생성
    return C3D_Job


def line_population_live(dong):     #남자 여자 상주인구 평균 ( 월 평균 시간대별 상주인구)
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []



    data = {}
    data["data1"] = []
    data["data2"] = []
    data["data3"] = []

    for i in range(8,21):
        query = f"select TIME, avg(TOTAL_P),M_sum,F_sum,H_DNG_NM from s_population a, H_CODE b  where  '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD and TIME= {i};"
        cursor = MySqlConn.makeCursor()
        cursor.execute(query)
        a = cursor.fetchone()

        # data 값 넣기
        data["data1"].append({"value": round(a[2])})
        data["data2"].append({"value": round(a[3])})
        data["data3"].append({"label": i})

    dataSource["dataset"].append({"seriesname": "남자", "data": data["data1"]})
    dataSource["dataset"].append({"seriesname": "여자", "data": data["data2"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    chartConfig["caption"] = "월평균 시간별 상주인구"
    chartConfig["xAxisName"] = '시간'
    chartConfig["yAxisName"] = "명"
    chartConfig["numberSuffix"] = "명"    # y축 숫자단위
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["bgcolor"] = '#f8f8ff'   # 차트 배경색 바꾸기
    chartConfig["plottooltext"] = "$label won <b>$dataValue</b> medals in $seriesName"

    # 그래프 특징 설정
    dataSource["chart"] = chartConfig
    dataSource["categories"].append({"category": data["data3"]})

    # print(dataSource)

    C3D = FusionCharts("msbar2d", "myFirstChart1", "450", "350", "park-2", "json", dataSource)
    # 그래프 생성
    return C3D


def age_population(dong):  #나이대 별 상주인구 수  (월 평균 나이대별 상주인구)
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []



    data = {}
    data["data1"] = []
    data["data2"] = []
    data["data3"] = []


    query = f"select date, (sum(M_20_to_24) + sum(M_25_to_29))/24, (sum(F_20_to_24) + sum(F_25_to_29))/24, (sum(M_30_to_34) + sum(M_35_to_39))/24, (sum(F_30_to_34) + sum(F_35_to_39))/24, (sum(M_40_to_44) + sum(M_45_to_49))/24," \
            f"(sum(F_40_to_44) + sum(F_45_to_49))/24,(sum(M_50_to_54) + sum(M_55_to_59))/24,(sum(F_50_to_54) + sum(F_55_to_59))/24 from s_population a, H_CODE b  where  '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD group by DATE;"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    # data 값 넣기
    data["data1"].append({"value": round(a[1])})
    data["data2"].append({"value": round(a[2])})
    data["data3"].append({"label": "20대"})
    data["data1"].append({"value": round(a[3])})
    data["data2"].append({"value": round(a[4])})
    data["data3"].append({"label": "30대"})
    data["data1"].append({"value": round(a[5])})
    data["data2"].append({"value": round(a[6])})
    data["data3"].append({"label": "40대"})
    data["data1"].append({"value": round(a[7])})
    data["data2"].append({"value": round(a[8])})
    data["data3"].append({"label": "50대"})

    dataSource["dataset"].append({"seriesname": "남자", "data": data["data1"]})
    dataSource["dataset"].append({"seriesname": "여자", "data": data["data2"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    chartConfig["caption"] = "일 평균 나이대별 상주인구"
    chartConfig["xAxisName"] = '시간'
    chartConfig["yAxisName"] = "명"
    chartConfig["numberSuffix"] = "명"    # y축 숫자단위
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["bgcolor"] = '#f8f8ff'   # 차트 배경색 바꾸기
    chartConfig["plotfillalpha"] = "80"

    # 그래프 특징 설정
    dataSource["chart"] = chartConfig
    dataSource["categories"].append({"category": data["data3"]})

    # print(dataSource)

    C3D = FusionCharts("mscolumn2d", "myFirstChart3", "450", "350", "park-3", "json", dataSource)
    # 그래프 생성
    return C3D


def chartjD(dong): #주택현황 파이그래프
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["data"] = []  # chartdata는 json형식이다.
    query = f"select sol_house, multi_gagu, dep_house, apartment, etc_house, multi_sede, non_live from seoul_house_dong where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    # data 값 넣기
    dataSource["data"].append({"label": '단독주택', "value": a[0]})
    dataSource["data"].append({"label": '다가구주택', "value": a[1]})
    dataSource["data"].append({"label": '영업겸용', "value": a[2]})
    dataSource["data"].append({"label": '아파트', "value": a[3]})
    dataSource["data"].append({"label": '연립주택', "value": a[4]})
    dataSource["data"].append({"label": '다세대주택', "value": a[5]})
    dataSource["data"].append({"label": '비거주용건물내주택', "value": a[6]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = "주택 현황"
    chartConfig["xAxisName"] = "주택 종류"
    chartConfig["yAxisName"] = "개수"
    chartConfig["numberSuffix"] = "개"  # y축 숫자단위
    chartConfig["theme"] = "fusion"  # 테마
    chartConfig["bgcolor"] = '#f8f8ff'

    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    C4D = FusionCharts("pie2d", "mySecondChart", "450", "350", "chart-2", "json", dataSource)
    # 그래프 생성
    return C4D


def chartmin1(dong): #세대수 피라미드
    dataSource = OrderedDict()
    dataSource["data"] = []  # chartdata는 json형식이다.
    query = f"select 1sede, 2sede, 3sede, 4sede, 5sede, 6sede, 7sede, 8sede, 9sede, 10sede from seoul_sede where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    dataSource["data"].append({"label": '1인세대', "value": a[0]})
    dataSource["data"].append({"label": '2인세대', "value": a[1]})
    dataSource["data"].append({"label": '3인세대', "value": a[2]})
    dataSource["data"].append({"label": '4인세대', "value": a[3]})
    dataSource["data"].append({"label": '5인세대', "value": a[4]})
    dataSource["data"].append({"label": '6인세대', "value": a[5]})
    dataSource["data"].append({"label": '7인세대', "value": a[6]})
    dataSource["data"].append({"label": '8인세대', "value": a[7]})
    dataSource["data"].append({"label": '9인세대', "value": a[8]})
    dataSource["data"].append({"label": '10인세대', "value": a[9]})

    chartConfig = OrderedDict()
    chartConfig["theme"] = "fusion"  # 테마
    chartConfig["caption"] = "세대수"
    chartConfig["showvalues"] = "1"
    chartConfig["numberSuffix"] = "trn"
    chartConfig["numberprefix"] = "$"
    chartConfig["plottooltext"] = "<b>$label</b> of world population owns <b>$dataValue</b> of global wealth"
    chartConfig["bgcolor"] = '#f8f8ff'


    dataSource["chart"] = chartConfig

    chartObj = FusionCharts('pyramid', 'ex1', '450', '350', 'min-1', 'json', dataSource)

    return chartObj




def grade(dong) -> dict:
    query = f"select dong, ((apartment / sum) * 100) + ((multi_sede / sum) * 100), ((sol_house / sum) * 100) + ((multi_gagu / sum) * 100) + ((etc_house / sum) * 100)," \
            f" ((dep_house / sum) * 100) + ((non_live / sum) * 100)from seoul_house_dong where dong = '{dong}';"
    query2 = f"select dong, hospital, bed from hospital where dong ='{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    cursor.execute(query2)
    b = cursor.fetchone()

    # g_point = None
    if b[1] > 0:
        if round(a[1]) >= 70:
            g_point = Mix(dong)
        else:
            g_point = hos(dong)
    else:
        if round(a[1]) >= 70:
            g_point = apt(dong)
        elif round(a[2]) >= 70:
            g_point = sol_house(dong)
        else:
            g_point = special(dong)

    return g_point


def text(dong):
    query = f"select sum(TOTAL_P)/744 from s_population a, H_CODE b where'{dong}' = b.H_DNG_NM and a.H_CD = b.H_DNG_CD;"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    total_p = round(a[0])

    return total_p


def special(dong):  #아파트도 아니고 단독주택도 아닌 특수 상권
    apt_u = "특수 상권"
    query = f"select sum(TOTAL_P)/744 from  s_population a, H_CODE b where '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD;"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()
    apt_dong = dong

    if round(a[0]) >= 15000:
        apt_grade = "우수 A급지"
    elif round(a[0]) >= 10000:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 20000:
        score = (round(a[0]) // 1000) * 0.1 + 13.5
    elif round(a[0]) >= 15000:
        score = (round(a[0]) // 1000)
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 1000)
    else:
        score = 20

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong': apt_dong, 'score': score}
    return psh


def Mix(dong):
    apt_u = '혼합형 상권'
    query = f"select sum(TOTAL_P)/744 from  s_population a, H_CODE b where '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD;"
    query2 = f"select dong, hospital, bed from hospital where dong ='{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    cursor.execute(query2)
    b = cursor.fetchone()
    apt_dong = dong

    if round(a[0]) >= 10000 and b[2] >= 400:
        apt_grade = "우수 A급지"
    elif round(a[0]) >= 6500 and b[2] >= 200:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 15000 and b[2] >= 400:  # "보통 A급지"
        score = (round(a[0]) // 1000) * 0.1 + 13.5
    elif round(a[0]) >= 8000 and b[2] >= 200:  # "보통 B급지"
        score = (round(a[0]) // 1000)
    elif round(a[0]) >= 0 and b[2] <= 200: # "불량 C급지"
        score = (round(a[0]) // 1000)
    else:
        score = 20

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong':apt_dong, 'score': score}
    return psh


def hos(dong):
    apt_u = '병원가 상권'
    query = f"select sum(TOTAL_P)/744 from  s_population a, H_CODE b where '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD;"
    query2 = f"select dong, hospital, bed from hospital where dong ='{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    cursor.execute(query2)
    b = cursor.fetchone()
    apt_dong = dong

    if round(a[0]) >= 12000 and b[2] >= 400:
        apt_grade = "우수 A급지"
    elif round(a[0]) >= 8000 and b[2] >= 200:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 9000 and b[2] >= 400:  # "보통 A급지"
        score = (round(a[0]) // 1000) * 0.1 + 13.5
    elif round(a[0]) >= 6000 and b[2] >= 200:  # "보통 B급지"
        score = (round(a[0]) // 1000)
    elif round(a[0]) >= 0 and b[2] <= 200:  # "불량 C급지"
        score = (round(a[0]) // 1000)
    else:
        score = 20

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong':apt_dong, 'score': score}
    return psh


def apt(dong) -> dict:
    apt_u = "아파트 상권"
    query = f"select sum(TOTAL_P)/744 from  s_population a, H_CODE b where '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD;"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()
    apt_dong = dong

    if round(a[0]) >= 12000:
        apt_grade = "우수 A급지"
    elif round(a[0]) >= 8000:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 14000:
        score = (round(a[0]) // 1000) * 0.1 + 13.5
    elif round(a[0]) >= 9000:
        score = (round(a[0]) // 1000)
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 1000)
    else:
        score = 20

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong': apt_dong, 'score': score}
    return psh


def sol_house(dong):
    apt_u = "단독주택 지역 상권"
    query = f"select sum(TOTAL_P)/744 from  s_population a, H_CODE b where '{dong}' = b.H_DNG_NM and a.H_CD =b.H_DNG_CD;"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()


    if a[0] >= 8000:
        apt_grade = "우수 A급지"
    elif a[0] >= 5000:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 14000:
        score = (round(a[0]) // 1000) * 0.1 + 13.5
    elif round(a[0]) >= 9000:
        score = (round(a[0]) // 1000)
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 1000)
    else:
        score = 20

    psh = {'apt_u': apt_u, 'apt_grade':apt_grade, 'score': score}
    return psh


def jipgaek(dong):
    query = f"select a.H_CD2, a.H_NM, a.L_PPL/b.area from S_population2 a, ppt_density b where a.H_NM = b.dong and b.dong = '{dong}';"
    query2 = f"select a.dong, a.all_sum/b.area from seoul_ppl_dong a, ppt_density b where a.dong = b.dong and b.dong = '{dong}';"
    query3 = f"select a.dong, a.sum/b.area from dong_job_ppt a, ppt_density b where a.dong = b.dong and b.dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()
    cursor.execute(query2)
    b = cursor.fetchone()
    cursor.execute(query3)
    c = cursor.fetchone()


    if 5000 <= round(a[2]):
        score1 = round((round(a[2]) // 1000)*0.1 + 3.5, 2)
    else:
        score1 = round((round(a[2]) // 1000)*0.1 + 2.9, 2)

    if round(b[1]) < 50000 :
        score2 = round((round(b[1]) // 1000)*0.1, 2)
    else:
        score2 = 5

    if round(c[1]) < 50000 :
        score3 = round((round(c[1]) // 1000)*0.1, 2)
    else:
        score3 = 5

    score4 = score1+ score2+ score3
    score5 = round(score4, 2)


    msj = {'score1':score1,'score2':score2,'score3':score3, 'score5':score5}
    return msj

def new(request):
    return render(request, 'chart.html')

def new1(request):
    map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=9)  # g.latlng [37.442803, 127.18161]
    plugins.LocateControl().add_to(map_osm)
    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    maps = map_osm._repr_html_()

    return render(request, 'index.html', {'map': maps})


