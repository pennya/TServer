from rest_framework import serializers

from api.models import Category, Restaurant, Distance, User, Version, Weather


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'email')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('c_id', 'name')

class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ('w_id', 'name')

class DistanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distance
        fields = ('d_id', 'name')

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    # owner = UserSerializer()
    # category = CategorySerializer()
    # weather = WeatherSerializer()
    # distance = DistanceSerializer()

    class Meta:
        model = Restaurant
        fields = ('owner','name', 'address', 'category', 'weather',
                  'distance', 'description')
        extra_kwargs = {
            'owner' : {'required' : True},
            'name' : {'required' : True},
            'category': {'required': True},
            'weather': {'required': True},
            'distance': {'required': True},
        }