# Create your views here.
import logging

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CategorySerializer
from .serializers import RestaurantSerializer
from .serializers import WeatherSerializer
from .serializers import DistanceSerializer
from .serializers import UserSerializer
from .serializers import VersionSerializer

from .forms import UserJoinForm
from .models import Category
from .models import Version
from .models import Restaurant
from .models import Distance
from .models import Weather
from .models import User

logger = logging.getLogger('test')


class VersionViewSet(viewsets.ModelViewSet):
    """
    version CRUD
    """
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        result = {}
        version = Version.objects.get(osType='android')

        result['result'] = 200
        result['osType'] = version.osType
        result['version'] = version.version
        return JsonResponse(result)


class UserViewSet(viewsets.ModelViewSet):
    """
    User CRUD
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    """
    login post
    """
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
    """
    recommand post
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        queryDict = request.POST
        category = queryDict.getlist('category')
        weather = queryDict.getlist('weather')
        distance = queryDict.getlist('distance')

        RestaurantList = Restaurant.objects.filter(category__in=category, weather__in=weather, distance__in=distance)
        restaurant_json = RestaurantSerializer(RestaurantList, many=True)
        return Response(restaurant_json.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class DistanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    restaurant CRUD
    but authorized user can only access create, update, delete method.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','weather',)

