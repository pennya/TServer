# Create your views here.
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.serializers import json
from rest_framework import filters
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .forms import UserJoinForm
from .models import Category, Restaurant, Weather, Distance, User, Version
from .serializers import CategorySerializer, RestaurantSerializer, WeatherSerializer, DistanceSerializer, \
    UserSerializer, VersionSerializer
from django.http import JsonResponse

import logging

logger = logging.getLogger('test')

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

"""
버전 테이블 뷰셋
버전 생성, 삭제, 업데이트, 리스트 가능
"""
class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        result = {}
        version = Version.objects.get(osType='android')

        result['result'] = 200
        result['osType'] = version.osType
        result['version'] = version.version
        return JsonResponse(result)
"""
유저 테이블 뷰셋
유저 생성, 삭제, 업데이트, 리스트 가능
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #parser_classes = (JSONParser)

    def create(self, request, *args, **kwargs):
        userForm = UserJoinForm(request.POST)
        result = {}
        idMultipleObject = True

        if userForm.is_valid():
            try:
                User.objects.get(id=userForm.data['id'])
                idMultipleObject = False
                User.objects.get(email=userForm.data['email'])
            except MultipleObjectsReturned as e:
                logger.error('join create error : ' + str(e))

                if idMultipleObject:
                    result['result'] = 411
                    result['message'] = 'id 중복'
                else:
                    result['result'] = 412
                    result['message'] = 'email 중복'

                return JsonResponse(result)
            except ObjectDoesNotExist:
                pass

            user = userForm.save()
            result['result'] = 200
            result['id'] = user.id
            result['password'] = user.password
            result['email'] = user.email

            return JsonResponse(result)
        else:
            logger.error('user join error : ')
            result['result'] = 410
            result['message'] = 'input form error'
            return JsonResponse(result)


"""
유저 테이블 뷰셋
유저 생성, 삭제, 업데이트, 리스트 가능
"""
class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        result = {}
        id = request.POST['id']
        password = request.POST['password']

        try:
            user = User.objects.get(id=id, password=password)
        except ObjectDoesNotExist:
            #messages.add_message(request, messages.INFO, '아이디 또는 비밀번호가 틀렸습니다')
            result['result'] = 410
            result['message'] = '아이디 또는 비밀번호가 틀렸습니다'
            return JsonResponse(result)

        result['result'] = 200
        result['id'] = user.id
        result['password'] = user.password
        result['email'] = user.email
        return JsonResponse(result)


class LoginView(views.APIView):
    def post(self, request, format=None):
        id = request.POST['id']
        password = request.POST['password']

        if User.objects.filter(id=id, password=password):
            return Response({
                'status' : 100
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status' : 101
            }, status=status.HTTP_200_OK)




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
        weather = self.get_object()
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

