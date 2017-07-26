# Create your views here.
import logging
import random

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CategorySerializer
from .serializers import RestaurantSerializer
from .serializers import WeatherSerializer
from .serializers import DistanceSerializer
from .serializers import UserSerializer
from .serializers import VersionSerializer
from .serializers import CommentSerializer
from .serializers import StarSerializer
from .serializers import HistorySerializer

from .forms import UserJoinForm

from .models import Category
from .models import Version
from .models import Restaurant
from .models import Distance
from .models import Weather
from .models import User
from .models import Comment
from .models import Star
from .models import History

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
        randomNum = random.randrange(0, RestaurantList.count())

        new_restaurant_list = []
        specific_restaurant = RestaurantList[randomNum]
        new_restaurant_list.append(specific_restaurant)

        restaurant_json = RestaurantSerializer(new_restaurant_list, many=True)
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
    """
    comment CRUD
    allow to make duplicate record in database.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant');

        if restaurant_id is not None:
            queryset = Comment.objects.filter(restaurant=restaurant_id)
        else:
            queryset = Comment.objects.all()

        return queryset


class StarViewSet(viewsets.ModelViewSet):
    """
    star CRUD
    not allow to make duplicate record in database
    """
    queryset = Star.objects.all()
    serializer_class = StarSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant')
        user_id = self.request.query_params.get('user')

        if restaurant_id is not None and user_id is not None:
            queryset = Star.objects.filter(restaurant=restaurant_id, user=user_id).distinct()
        else:
            queryset = Star.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        result = {}

        star_obj = self.get_queryset()
        if star_obj.count() != 0:
            star_json = StarSerializer(star_obj, many=True).data
            result.update({
                'result' : star_json
            })
        else:
            result.update({
                'result': 414,
                'message': 'could not find any matched content',
            })

        return Response(result)

    def create(self, request, *args, **kwargs):
        result = {}

        restaurant_id = request.data['restaurant']
        user_id = request.data['user']

        star_obj = Star.objects.filter(restaurant=restaurant_id, user=user_id)
        if star_obj.count() == 0:
            return super().create(request)

        else:
            result.update({
                'result' : 415,
                'message': 'There is duplicate record.',
            })
            return Response(result)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')

        if user_id is not None:
            queryset = History.objects.filter(user=user_id)
        else:
            queryset = History.objects.all()

        return queryset
