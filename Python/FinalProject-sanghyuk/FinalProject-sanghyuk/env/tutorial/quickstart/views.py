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

#기본 html
def graph(request):
    return render(request, 'chart.html')

def main(request):
    map_osm = folium.Map(location=[37.442803, 127.18161], zoom_start=9)  # g.latlng [37.442803, 127.18161]
    plugins.LocateControl().add_to(map_osm)
    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    maps = map_osm._repr_html_()

    return render(request, 'main.html', {'map': maps})


#################################################################################################################


class AAViewSet(viewsets.ModelViewSet):
    queryset = AA.objects.all()
    serializer_class = AASerializer

#지도 그리기
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


#업종 현황 선택박스 post 함수
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


#분석결과 선택박스 post 함수
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
        gumaegu = gumae(dong)
        jipgaek1 = jipgaek(dong)
        choii = Anjung(dong)
        choi = chart3D_Job(dong)
        minn2 = jipgaek_radar(dong)
        minn1 = gumae_radar(dong)
        cchoi = Anjung_radar(dong)
        all_summ = all_sum(dong)
        rader_choi = sang_radar(dong)
        transport_a = T_S.transport(dong)
        subway_a = T_S.subway(dong)
        sang = sum_T_S(dong)
        safe = safe_op(dong)
        close = safe_cl(dong)


        # park_grade = score_G(dong)
        return render(request, 'chart.html',
                      {'output': column3D.render(), 'output2': column2D.render(), 'output3': mscolumn2d.render(),
                       'apt_u': g_point['apt_u'], 'apt_grade': g_point['apt_grade'], 'apt_dong': g_point['apt_dong'],
                       'score': g_point['score'], 'total_p': total_p,
                       'output4': sede.render(), 'output5': jutaek.render(), 'output6': choi.render(), 'output7' : minn2.render(), 'output8': minn1.render(), 'output9':cchoi.render(), 'all_sum':all_summ, 'rader_1':rader_choi.render(),
                       'transport': transport_a, 'subway': subway_a, 'sang1': sang, 'safe1': safe.render(), 'close1':close.render(),
                       'M_score1':gumaegu['M_score1'],'M_score2':gumaegu['M_score2'],'M_score3':gumaegu['M_score3'],'M_score5':gumaegu['M_score5'],
                       'J_score1':jipgaek1['J_score1'],'J_score2':jipgaek1['J_score2'],'J_score3':jipgaek1['J_score3'],'J_score5':jipgaek1['J_score5'],
                       'changed_grade':choii['changed_grade'],'operation_grade':choii['operation_grade'],'closing_grade':choii['closing_grade'], 'score_sum':choii['score_sum']})  # render


############################################################################################################


#그래프 함수
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


def chart3D_Job(dong):  #요일별 상주인구
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data1"] = []
    # data["data2"] = []


    query1 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220117' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query2 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220118' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query3 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220119' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query4 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220120' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query5 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220121' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query6 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220122' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    query7 = f"select sum(TOTAL_P)/24 from s_population a, H_CODE b where DATE = '20220123' and a.H_CD = b.H_DNG_CD and b.H_DNG_NM = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query1)
    a = cursor.fetchone()
    cursor.execute(query2)
    b = cursor.fetchone()
    cursor.execute(query3)
    c = cursor.fetchone()
    cursor.execute(query4)
    d = cursor.fetchone()
    cursor.execute(query5)
    e = cursor.fetchone()
    cursor.execute(query6)
    f = cursor.fetchone()
    cursor.execute(query7)
    g = cursor.fetchone()


    # data 값 넣기
    data["data1"].append({"value": round(a[0])})
    data["data1"].append({"value": round(b[0])})
    data["data1"].append({"value": round(c[0])})
    data["data1"].append({"value": round(d[0])})
    data["data1"].append({"value": round(e[0])})
    data["data1"].append({"value": round(f[0])})
    data["data1"].append({"value": round(g[0])})
    # data["data2"].append({"value": a[1]})
    # data["data2"].append({"value": a[3]})
    # data["data2"].append({"value": a[5]})
    # data["data2"].append({"value": a[7]})

    dataSource["dataset"].append({"seriesname": f"{dong}", "data": data["data1"]})
    # dataSource["dataset"].append({"seriesname": "서울 평균 운영 개월 수", "data": data["data2"]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = "요일 별 평균 상주인구"
    # chartConfig["xAxisName"] = "요일"
    # chartConfig["yAxisName"] = "점포 수"
    chartConfig["numberSuffix"] = "명"  # y축 숫자단위
    chartConfig["bgcolor"] = '#f8f8ff'
    chartConfig["theme"] = "fusion"  # 테마
    chartConfig["drawcrossline"] = 1
    chartConfig["showhovereffect"] = 1
    chartConfig["plottooltext"] = "<b>$dataValue</b> of youth were on $seriesName"


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig
    categories["category"].append({"label": "월"})
    categories["category"].append({"label": "화"})
    categories["category"].append({"label": "수"})
    categories["category"].append({"label": "목"})
    categories["category"].append({"label": "금"})
    categories["category"].append({"label": "토"})
    categories["category"].append({"label": "일"})
    dataSource["categories"].append({"category": categories["category"]})

    # print(dataSource["dataset"])

    C3D_Job = FusionCharts("msline", "parkChart3", "450", "350", "choi-2", "json", dataSource)
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


def jipgaek_radar(dong): #집객력 radar그래프
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data"] = []

    categories["category"].append({"label": "유동인구"})
    categories["category"].append({"label": "배후 주거인구"})
    categories["category"].append({"label": "배후 직장인구"})

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
        J_score1 = round((round(a[2]) // 1000) * 0.1 + 3.5, 2)
    else:
        J_score1 = round((round(a[2]) // 1000) * 0.1 + 2.9, 2)

    if round(b[1]) < 50000:
        J_score2 = round((round(b[1]) // 1000) * 0.1, 2)
    else:
        J_score2 = 5

    if round(c[1]) < 50000:
        J_score3 = round((round(c[1]) // 1000) * 0.1, 2)
    else:
        J_score3 = 5

    J_score1 = round(J_score1, 2)
    J_score2 = round(J_score2, 2)
    J_score3 = round(J_score3, 2)
    J_score4 = J_score1 + J_score2 + J_score3
    J_score5 = round(J_score4, 2)



    data["data"].append({"value": J_score1})
    data["data"].append({"value": J_score2})
    data["data"].append({"value": J_score3})
    dataSource["dataset"].append({"seriesname": "User Ratings", "data": data["data"]})
    dataSource["categories"].append({"category":categories["category"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["showlegend"] = "0"
    chartConfig["showdivlinevalues"] = "0"
    chartConfig["showlimits"] = "0"
    chartConfig["showvalues"] = "1"
    chartConfig["plotfillalpha"] = "40"
    chartConfig["plottooltext"] = f"'{dong}'<b>$label</b> grade is rated as <b>$value</b>"


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    # print(dataSource["categories"])
    # print(dataSource["dataset"])

    C3D = FusionCharts("radar", "ex2", "400", "400", "minn-2", "json", dataSource)
    # 그래프 생성
    return C3D


def gumae_radar(dong): #집객력 radar그래프
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data"] = []

    categories["category"].append({"label": "매출규모"})
    categories["category"].append({"label": "직장인구"})
    categories["category"].append({"label": "주거인구"})

    query = f"select b.dong, a.SALE_SUM/(b.area*100) from S_mechul a, ppt_density b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    query2 = f"select b.dong, a.SALE_SUM/b.sum from S_mechul a, dong_job_ppt b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    query3 = f"select b.dong, a.SALE_SUM/b.all_sum from S_mechul a, seoul_ppl_dong b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()
    cursor.execute(query2)
    b = cursor.fetchone()
    cursor.execute(query3)
    c = cursor.fetchone()

    if round(a[1]) < 97000:
        M_score1 = round(round(a[1])) * 0.0001
    else:
        M_score1 = 9.7

    if round(b[1]) < 1000:
        M_score2 = round(round(b[1])) * 0.001
    else:
        M_score2 = 5

    if round(c[1]) < 500:
        M_score3 = round(round(c[1])) * 0.01
    else:
        M_score3 = 5

    M_score1 = round(M_score1, 2)
    M_score2 = round(M_score2, 2)
    M_score3 = round(M_score3, 2)
    M_score4 = M_score1 + M_score2 + M_score3
    M_score5 = round(M_score4, 2)



    data["data"].append({"value": M_score1})
    data["data"].append({"value": M_score2})
    data["data"].append({"value": M_score3})
    dataSource["dataset"].append({"seriesname": "User Ratings", "data": data["data"]})
    dataSource["categories"].append({"category":categories["category"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["showlegend"] = "0"
    chartConfig["showdivlinevalues"] = "0"
    chartConfig["showlimits"] = "0"
    chartConfig["showvalues"] = "1"
    chartConfig["plotfillalpha"] = "40"
    chartConfig["plottooltext"] = f"'{dong}'<b>$label</b> grade is rated as <b>$value</b>"


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    # print(dataSource["categories"])
    # print(dataSource["dataset"])

    C3D = FusionCharts("radar", "ex3", "400", "400", "minn-1", "json", dataSource)
    # 그래프 생성
    return C3D


def Anjung_radar(dong): #안정성 radar그래프
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data"] = []

    categories["category"].append({"label": "변동성"})
    categories["category"].append({"label": "운영연수"})
    categories["category"].append({"label": "휴/폐업률"})

    query = f"select change_21_3,operation_21_3,closing_21_3 from dong_operation where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    if a[0] == 'LH':
        changed_grade = 10
    elif a[0] == 'LL':
        changed_grade = 7.5
    elif a[0] == 'HH':
        changed_grade = 5
    else:
        changed_grade = 2.5
    if a[1] >= 144:
        operation_grade = 5
    elif 123 <= a[1] < 144:
        operation_grade = 4
    elif 115 <= a[1] < 123:
        operation_grade = 3
    elif 108 <= a[1] < 115:
        operation_grade = 2
    else:
        operation_grade = 1
    if a[2] >= 67:
        closing_grade = 5
    elif 57 <= a[2] < 67:
        closing_grade = 4
    elif 54 <= a[2] < 57:
        closing_grade = 3
    elif 52 <= a[2] < 54:
        closing_grade = 2
    else:
        closing_grade = 1

    data["data"].append({"value": changed_grade})
    data["data"].append({"value": operation_grade})
    data["data"].append({"value": closing_grade})
    dataSource["dataset"].append({"seriesname": "User Ratings", "data": data["data"]})
    dataSource["categories"].append({"category":categories["category"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["showlegend"] = "0"
    chartConfig["showdivlinevalues"] = "0"
    chartConfig["showlimits"] = "0"
    chartConfig["showvalues"] = "1"
    chartConfig["plotfillalpha"] = "40"
    chartConfig["plottooltext"] = f"'{dong}'<b>$label</b> grade is rated as <b>$value</b>"


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    # print(dataSource["categories"])
    # print(dataSource["dataset"])

    C3D = FusionCharts("radar", "ex4", "400", "400", "cchoi-1", "json", dataSource)
    # 그래프 생성
    return C3D


def sang_radar(dong): #rader 그래프 접근성
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data"] = []

    categories["category"].append({"label": "상권 점수"})
    categories["category"].append({"label": "버스 이용자 수"})
    categories["category"].append({"label": "지하철 이용자 수"})

    bus_score = T_S.subway(dong)
    subway_score = T_S.transport(dong)
    a_score = grade(dong)["score"]


    data["data"].append({"value": a_score})
    data["data"].append({"value": subway_score})
    data["data"].append({"value": bus_score})
    dataSource["dataset"].append({"seriesname": "User Ratings", "data": data["data"]})
    dataSource["categories"].append({"category":categories["category"]})

    chartConfig = OrderedDict()
    # chartConfig = {}
    # chartConfig["caption"] = f"Skill Analysis of Harry'{dong}'"
    # chartConfig["subCaption"] = "Scale: 1 (low) to 10 (high)"
    chartConfig["theme"] = "fusion"      # 테마
    chartConfig["showlegend"] = "0"
    chartConfig["showdivlinevalues"] = "0"
    chartConfig["showlimits"] = "0"
    chartConfig["showvalues"] = "1"
    chartConfig["plotfillalpha"] = "40"
    chartConfig["plottooltext"] = f"'{dong}'<b>$label</b> grade is rated as <b>$value</b>"
    chartConfig["bgcolor"] = '#f8f8ff'


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    # print(dataSource["categories"])
    # print(dataSource["dataset"])

    C3D = FusionCharts("radar", "ex9", "400", "400", "choi-5", "json", dataSource)
    # 그래프 생성
    return C3D


def safe_op(dong):  #운영 개월수
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["data"] = []  # chartdata는 json형식이다.
    query1 = f"select operation_21_1,seoul_operation_21_1 from  dong_operation where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query1)
    a = cursor.fetchone()

    # data 값 넣기
    dataSource["data"].append({"label": f"{dong} 평균 운영 개월 수", "value": a[0]})
    dataSource["data"].append({"label": "서울 평균 운영 개월 수", "value": a[1]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = "운영 개월 수"
    # chartConfig["xAxisName"] = "x축이름"
    # chartConfig["yAxisName"] = "개월 수"
    chartConfig["numberSuffix"] = "개월"  # y축 숫자단위
    chartConfig["bgcolor"] = '#f8f8ff'
    chartConfig["theme"] = "fusion"  # 테마


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig

    C3D_Job = FusionCharts("column2d", "parkChart2", "450", "350", "choi-3", "json", dataSource)
    # 그래프 생성
    return C3D_Job


def safe_cl(dong):  #안정성 근거(폐업률)
    # chartdata 선언
    dataSource = OrderedDict()
    dataSource["dataset"] = []
    dataSource["categories"] = []
    categories = OrderedDict()
    categories["category"] = []
    data = {}
    data["data1"] = []
    data["data2"] = []

    query1 = f"select closing_21_1 , seoul_closing_21_1,closing_21_2,seoul_closing_21_2,closing_21_3," \
             f"seoul_closing_21_3,closing_20_4,seoul_closing_20_4 from dong_operation where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query1)
    a = cursor.fetchone()

    # data 값 넣기
    data["data1"].append({"value": a[0]})
    data["data1"].append({"value": a[2]})
    data["data1"].append({"value": a[4]})
    data["data1"].append({"value": a[6]})
    data["data2"].append({"value": a[1]})
    data["data2"].append({"value": a[3]})
    data["data2"].append({"value": a[5]})
    data["data2"].append({"value": a[7]})

    dataSource["dataset"].append({"seriesname": f"{dong} 평균 폐업 가게 수", "data": data["data1"]})
    dataSource["dataset"].append({"seriesname": "서울 평균 폐업 수", "data": data["data2"]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = "폐업 가게 수"
    # chartConfig["xAxisName"] = "x축이름"
    chartConfig["yAxisName"] = "점포 수"
    chartConfig["numberSuffix"] = "개"  # y축 숫자단위
    chartConfig["bgcolor"] = '#f8f8ff'
    chartConfig["theme"] = "fusion"  # 테마
    chartConfig["drawcrossline"] = 1
    chartConfig["showhovereffect"] = 1
    chartConfig["plottooltext"] = "<b>$dataValue</b> of youth were on $seriesName"


    # 그래프 특징 설정
    dataSource["chart"] = chartConfig
    categories["category"].append({"label": "1분기"})
    categories["category"].append({"label": "2분기"})
    categories["category"].append({"label": "3분기"})
    categories["category"].append({"label": "4분기"})
    dataSource["categories"].append({"category": categories["category"]})

    # print(dataSource["dataset"])

    C3D_Job = FusionCharts("msline", "choiChart4", "450", "350", "choi-4", "json", dataSource)
    # 그래프 생성
    return C3D_Job
############################################################################################################


#점수화 함수
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
        apt_grade = "미달 C급지"

    if round(a[0]) >= 20000:
        score = (round(a[0]) // 1000) * 0.1 + 5
    elif round(a[0]) >= 15000:
        score = (round(a[0]) // 500) * 0.1 + 1.5
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 500) * 0.1 + 1.1
    else:
        score = 10

    sang_score = round(score, 2)

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong': apt_dong, 'score': sang_score}
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

    if round(a[0]) >= 10000 and b[2] >= 200:
        apt_grade = "우수 A급지"
    elif round(a[0]) >= 6500 and b[2] >= 100:
        apt_grade = "보통 B급지"
    else:
        apt_grade = "불량 C급지"

    if round(a[0]) >= 15000 and b[2] >= 400:  # "보통 A급지"
        score = (round(a[0]) // 1000) * 0.1 + 5.5
    elif round(a[0]) >= 8000 and b[2] >= 200:  # "보통 B급지"
        score = (round(a[0]) // 500) * 0.1 + 3.6
    elif round(a[0]) >= 0 and b[2] <= 200: # "불량 C급지"
        score = (round(a[0]) // 500) * 0.1 + 2.5
    else:
        score = 10

    sang_score = round(score, 2)

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong':apt_dong, 'score': sang_score}
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
        score = (round(a[0]) // 1000) * 0.1 + 6.1
    elif round(a[0]) >= 5000 and b[2] >= 200:  # "보통 B급지"
        score = (round(a[0]) // 500) * 0.1 + 3
    elif round(a[0]) >= 0 and b[2] <= 200:  # "불량 C급지"
        score = (round(a[0]) // 500) * 0.2 + 1.9
    else:
        score = 10

    sang_score = round(score, 2)

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong':apt_dong, 'score': sang_score}
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

    if round(a[0]) >= 15000:
        score = (round(a[0]) // 1000) * 0.1 + 5.5
    elif round(a[0]) >= 8000:
        score = (round(a[0]) // 500) * 0.1 + 3.6
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 500) * 0.1 + 2.5
    else:
        score = 10

    sang_score = round(score, 2)

    psh = {'apt_u': apt_u, 'apt_grade': apt_grade, 'apt_dong': apt_dong, 'score': sang_score}
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

    if round(a[0]) >= 15000:
        score = (round(a[0]) // 1000) * 0.1 + 5.5
    elif round(a[0]) >= 8000:
        score = (round(a[0]) // 500) * 0.1 + 3.6
    elif round(a[0]) >= 0:
        score = (round(a[0]) // 500) * 0.1 + 2.5
    else:
        score = 10

    sang_score = round(score, 2)

    psh = {'apt_u': apt_u, 'apt_grade':apt_grade, 'score': sang_score}
    return psh


def jipgaek(dong): #집객력 점수
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
        J_score1 = round((round(a[2]) // 1000)*0.1 + 3.5, 2)
    else:
        J_score1 = round((round(a[2]) // 1000)*0.1 + 2.9, 2)

    if round(b[1]) < 50000 :
        J_score2 = round((round(b[1]) // 1000)*0.1, 2)
    else:
        J_score2 = 5

    if round(c[1]) < 50000 :
        J_score3 = round((round(c[1]) // 1000)*0.1, 2)
    else:
        J_score3 = 5

    J_score1 = round(J_score1,2)
    J_score2 = round(J_score2, 2)
    J_score3 = round(J_score3, 2)
    J_score4 = J_score1+ J_score2+ J_score3
    J_score5 = round(J_score4, 2)


    msj = {'J_score1':J_score1,'J_score2':J_score2,'J_score3':J_score3, 'J_score5':J_score5}
    return msj


def gumae(dong): #구매력 점수
    query = f"select b.dong, a.SALE_SUM/(b.area*100) from S_mechul a, ppt_density b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    query2 = f"select b.dong, a.SALE_SUM/b.sum from S_mechul a, dong_job_ppt b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    query3 = f"select b.dong, a.SALE_SUM/b.all_sum from S_mechul a, seoul_ppl_dong b where a.H_DNG_NM = b.dong and b.dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()
    cursor.execute(query2)
    b = cursor.fetchone()
    cursor.execute(query3)
    c = cursor.fetchone()


    if round(a[1]) < 97000 :
        M_score1 = round(round(a[1]))*0.0001
    else:
        M_score1 = 9.7

    if round(b[1]) < 1000 :
        M_score2 = round(round(b[1]))*0.001
    else:
        M_score2 = 5

    if round(c[1]) < 500 :
        M_score3 = round(round(c[1]))*0.01
    else:
        M_score3 = 5

    M_score1 = round(M_score1,2)
    M_score2 = round(M_score2, 2)
    M_score3 = round(M_score3, 2)
    M_score4 = M_score1 + M_score2 + M_score3
    M_score5 = round(M_score4, 2)

    msj2 = {'M_score1': M_score1, 'M_score2': M_score2, 'M_score3': M_score3, 'M_score5': M_score5}

    return msj2


def Anjung(dong): #안정성 점수
    query = f"select change_21_3,operation_21_3,closing_21_3 from dong_operation where dong = '{dong}';"
    cursor = MySqlConn.makeCursor()
    cursor.execute(query)
    a = cursor.fetchone()

    if a[0] == 'LH':
        changed_grade = 10
    elif a[0] == 'LL':
        changed_grade = 7.5
    elif a[0] == 'HH':
        changed_grade = 5
    else:
        changed_grade = 2.5
    if a[1] >= 144:
        operation_grade = 5
    elif 123 <= a[1] < 144:
        operation_grade = 4
    elif 115 <= a[1] < 123:
        operation_grade = 3
    elif 108 <= a[1] < 115:
        operation_grade = 2
    else:
        operation_grade = 1
    if a[2] >= 67:
        closing_grade = 5
    elif 57 <= a[2] < 67:
        closing_grade = 4
    elif 54 <= a[2] < 57:
        closing_grade = 3
    elif 52 <= a[2] < 54:
        closing_grade = 2
    else:
        closing_grade = 1

    score_sum = changed_grade + operation_grade + closing_grade
    choi = {'changed_grade':changed_grade, 'operation_grade':operation_grade,'closing_grade':closing_grade, 'score_sum': score_sum}

    return choi


class T_S: #접근성 점수


    @staticmethod
    def transport(dong):  # 접근성 버스 점수 (0~5점)
        query = f"select (sum(P_C))/31 from transport a , H_CODE b where a.H_SDNG_CD = b.H_SDNG_CD and b.H_DNG_NM ='{dong}';"
        cursor = MySqlConn.makeCursor()
        cursor.execute(query)
        a = cursor.fetchone()

        score2 = (round(a[0]) // 3000) * 0.1
        score3 = round(score2, 2)

        return score3

    @staticmethod
    def subway(dong):  # 접근성 지하철 점수 (0~5점)
        query = f"select (sum(S_P_C))/31 from Subway a , H_CODE b where a.H_SDG_CD = b.H_SDNG_CD and b.H_DNG_NM ='{dong}';"
        cursor = MySqlConn.makeCursor()
        cursor.execute(query)
        a = cursor.fetchone()

        if a[0] < 150000:
            score3 = (round(a[0]) // 2000) * 0.1  # 하루 평균 지하철 이용자 수
        else:
            score3 = 5

        score4 = round(score3)
        return score4


def abc(request):
    return render(request, 'table.html')

def all_sum(dong):

    all_summ = round(gumae(dong)['M_score5'] + jipgaek(dong)['J_score5'] + Anjung(dong)['score_sum'] + T_S.subway(dong) + T_S.transport(dong) + grade(dong)["score"],2)
    return all_summ

def sum_T_S(dong):
    T_S_score = round(T_S.subway(dong) + T_S.transport(dong) + grade(dong)["score"], 2)

    return T_S_score
