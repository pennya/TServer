# Create your views here.
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Category, Restaurant, Weather, Distance, User, Version
from .serializers import CategorySerializer, RestaurantSerializer, WeatherSerializer, DistanceSerializer, \
    UserSerializer, VersionSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import logging

logger = logging.getLogger('test')

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

"""
버전 테이블 뷰셋
버전 생성, 삭제, 업데이트, 리스트 가능
"""
class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset1 = Version.objects.all()
    #     logger.info('version list info')
    #     logger.debug('version list debug')
    #     logger.error('version list error')
    #     serializer1 = VersionSerializer(queryset1)
    #
    #     return Response(self.get_serializer())

    def create(self, request, *args, **kwargs):
        aaa = request.data

        logger.error('version create abc : '+aaa['abc'])
        logger.error('version create abcd : ' + aaa['abcd'])

        #ddaa = ['aaa':111, 'bbb':222]

        return Response({'a': 11})

    def retrieve(self, request, *args, **kwargs):
        logger.error('version retrieve')
"""
유저 테이블 뷰셋
유저 생성, 삭제, 업데이트, 리스트 가능
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
카테고리 테이블 읽기전용 뷰셋
카테고리 읽기 가능
"""
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

"""
날씨 테이블 읽기전용 뷰셋
날씨 읽기 가능
"""
class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    #지정된 날씨가 등록된 음식점 찾기
    @detail_route()
    def restaurant_list(self, request, pk=None):
        weather = self.get_object();
        restaurant = Restaurant.objects.filter(weather= weather)
        restaurant_json = RestaurantSerializer(restaurant, many=True)
        return Response(restaurant_json.data)

"""
거리 테이블 읽기전용 뷰셋
거리 읽기 가능
"""
class DistanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer

"""
음식점 테이블 뷰셋
음식점 생성, 삭제, 업데이트, 리스트 가능
등록자만 생성, 업데이트, 삭제 가능
"""
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','weather',)

