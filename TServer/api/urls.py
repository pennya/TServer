from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from TServer.api import views

router = routers.DefaultRouter()
router.register(r'versions', views.VersionViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'login', views.LoginViewSet)
router.register(r'categorys', views.CategoryViewSet)
router.register(r'weathers', views.WeatherViewSet)
router.register(r'distances', views.DistanceViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'recommands', views.RecommandViewSet)

schema_view = get_swagger_view(title='TServer API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs$', schema_view),
    url(r'^api-v1/', include('rest_framework.urls', namespace='rest_framework_category')),
]