from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api.views import VersionViewSet
from api.views import UserViewSet
from api.views import LoginViewSet
from api.views import CategoryViewSet
from api.views import WeatherViewSet
from api.views import DistanceViewSet
from api.views import RestaurantViewSet
from api.views import RecommandViewSet
from api.views import CommentViewSet
from api.views import StarViewSet
from api.views import ParticularStarViewSet


router = routers.DefaultRouter()
router.register(r'versions', VersionViewSet, base_name='versions')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'logins', LoginViewSet, base_name='logins')
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'weathers', WeatherViewSet, base_name='weathers')
router.register(r'distances', DistanceViewSet, base_name='distances')
router.register(r'restaurants', RestaurantViewSet, base_name='restaurants')
router.register(r'recommands', RecommandViewSet, base_name='recommands')
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'stars', StarViewSet, base_name='stars')
router.register(r'detail_stars', ParticularStarViewSet, base_name='detail_stars')

schema_view = get_swagger_view(title='TServer API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs$', schema_view),
    url(r'^api-v1/', include('rest_framework.urls', namespace='rest_framework_category')),
]