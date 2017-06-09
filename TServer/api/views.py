# Create your views here.
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.models import Category, Restaurant, Weather, Distance, User, Version
from api.serializers import CategorySerializer, RestaurantSerializer, WeatherSerializer, DistanceSerializer, \
    UserSerializer, VersionSerializer


"""
버전 테이블 뷰셋
버전 생성, 삭제, 업데이트, 리스트 가능
"""
class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

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

