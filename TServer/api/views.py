# Create your views here.
import logging

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import CategorySerializer
from .serializers import RestaurantSerializer
from .serializers import WeatherSerializer
from .serializers import DistanceSerializer
from .serializers import UserSerializer
from .serializers import VersionSerializer
from .serializers import CommentSerializer
from .serializers import StarSerializer

from .forms import UserJoinForm
from .forms import StarForm

from .models import Category, RestaurantImage
from .models import Version
from .models import Restaurant
from .models import Distance
from .models import Weather
from .models import User
from .models import Comment
from .models import Star
from .models import RestaurantMap

logger = logging.getLogger('test')

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        result = {}
        version = Version.objects.get(osType='android')

        result['osType'] = version.osType
        result['versionCode'] = version.versionCode
        result['versionName'] = version.versionName
        return JsonResponse(result)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        userForm = UserJoinForm(request.data)
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

                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                pass

            user = userForm.save()
            result['id'] = user.id
            result['password'] = user.password
            result['email'] = user.email

            return JsonResponse(result)
        else:
            logger.error('user join error : ')
            result['result'] = 410
            result['message'] = 'input form error'
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        result = {}
        id = request.data['id']
        password = request.data['password']

        try:
            user = User.objects.get(id=id, password=password)
        except ObjectDoesNotExist:
            #messages.add_message(request, messages.INFO, '아이디 또는 비밀번호가 틀렸습니다')
            result['result'] = 410
            result['message'] = '아이디 또는 비밀번호가 틀렸습니다'
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)
        except MultipleObjectsReturned:
            result['result'] = 411
            result['message'] = '동일한 유저 정보 다수 존재합니다.'
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

        #result['result'] = status.HTTP_200_OK
        result['id'] = user.id
        result['password'] = user.password
        result['email'] = user.email
        return JsonResponse(result)


class RecommandViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        queryDict = request.data
        category = queryDict.getlist('category')
        weather = queryDict.getlist('weather')
        distance = queryDict.getlist('distance')

        RestaurantList = Restaurant.objects.filter(category__in=category, weather__in=weather, distance__in=distance)
        restaurant_json = RestaurantSerializer(RestaurantList, many=True)
        return Response(restaurant_json.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class DistanceViewSet(viewsets.ModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    restaurant CRUD
    but authorized user can only access create, update, delete method.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class StarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer


class ParticularStarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer

    def create(self, request, *args, **kwargs):
        result = {}
        restaurant = request.data['restaurant']
        user = request.data['user']
        star_list = Star.objects.filter(restaurant=restaurant, user=user).distinct()

        if star_list.count() == 0:
            result['result'] = 414
            result['message'] = 'could not find any matched content'
            return JsonResponse(result)

        star_json = StarSerializer(star_list, many=True)
        return Response(star_json.data)

class RestaurantDetailInfoViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        result = {}
        restaurantId = request.data['id']
        userId = request.data['userId']
        print('res id : '+str(restaurantId))
        print('user id : '+str(userId))
        restaurantInfo = Restaurant.objects.filter(id=restaurantId)
        print(str(11111111111111))
        star_list = Star.objects.filter(restaurant=restaurantId)
        print(str(222222222222222))
        ratingAverageValue = 0

        for i in star_list:
            ratingAverageValue += i.rating

        ratingAverageValue = ratingAverageValue / star_list.count()
        userRatingValue = Star.objects.filter(restaurant=restaurantId, user=userId)
        comment_list = Comment.objects.filter(restaurant=restaurantId).all()
        mapInfo = RestaurantMap.objects.filter(restaurant=restaurantId)

        images = RestaurantImage.objects.filter(restaurant=restaurantId)


        #detailRestaurant = serializers.serialize("json", restaurantInfo)
        # restaurantMap = serializers.serialize('json', mapInfo)
        restaurantImages = serializers.serialize("json", images)
        #json = JSONRenderer().render(restaurantImages)


        #print(str(detailRestaurant))
        #return HttpResponse(restaurantImages, content_type='application/json')
        return JsonResponse(images)
        # return Response({
        #     'cart': cart_serializer.data,
        #     'another': another_serializer.data,
        #     'yet_another_field': 'yet another value',
        # })


        # #
        # 이름
        # 주소
        # 카테고리
        # 날씨
        # 거리
        # 설명
        # 별점
        # 댓그카운트
        # 이미지리스트
        # 위도
        # 경도#

        if star_list.count() == 0:
            result['result'] = 414
            result['message'] = 'could not find any matched content'
            return JsonResponse(result)

        star_json = StarSerializer(star_list, many=True)
        return Response(star_json.data)