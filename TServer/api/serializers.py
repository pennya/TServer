from rest_framework import serializers

from api.models import Category, Restaurant, Distance, User


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
        model = Category
        fields = ('w_id', 'name')

class DistanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distance
        fields = ('d_id', 'name')

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
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