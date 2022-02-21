from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from quickstart import views  # 이 부분 수정함
from django.urls import path, include

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'AAs', views.AAViewSet)
# router.register(r'posts', views.PostViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('post', views.PostAPIView.as_view()),   #지역/상권업종 선택해서 post하는 화면
    path('chart', views.ChartAPIView.as_view()), #지역선택 post해서 차트 그려주는 화면
    # path('dash', views.chart_VIEW.as_view()),
    path('graph', views.graph),
    path('main', views.main),
    path('abc', views.abc),
]