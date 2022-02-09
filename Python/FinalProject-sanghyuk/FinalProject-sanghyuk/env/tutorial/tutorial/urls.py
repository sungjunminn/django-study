from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from quickstart import views  # 이 부분 수정함
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'AAs', views.AAViewSet)
# router.register(r'posts', views.PostViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('index',views.index),
    path('home',views.home),
    path('post', views.PostAPIView.as_view()),
    # path('show',views.show),
    # path('aa',views.aa),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('asdf', views.asdf),
    path('jkl', views.PostAPIView.as_view()),
    path('qwer', views.qwer),
    path('abc', views.abc),
    path('test', views.test),
    path('dash', views.chart_VIEW.as_view()),
    path('dashmap', views.dashmap),
    path('dashmap2', views.dashmap2),
    path('chart', views.ChartAPIView.as_view()),
]