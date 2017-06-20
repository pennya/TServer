from rest_framework import serializers

from .models import Category, Restaurant, Distance, User, Version, Weather

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('c_id', 'name')

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('w_id', 'name')

class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distance
        fields = ('d_id', 'name')

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'category', 'weather',
                  'distance', 'description')
        extra_kwargs = {
            'name' : {'required' : True},
            'category': {'required': True},
            'weather': {'required': True},
            'distance': {'required': True},
        }