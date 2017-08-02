from rest_framework import serializers

from .models import Category
from .models import Restaurant
from .models import Distance
from .models import User
from .models import Version
from .models import Weather
from .models import Comment
from .models import Star
from .models import History


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('versionCode', 'versionName', 'osType', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('u_id', 'id', 'password', 'email', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('c_id', 'name', )


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('w_id', 'name', )


class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distance
        fields = ('d_id', 'name', )


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'category', 'weather',
                  'distance', 'description', )
        extra_kwargs = {
            'name' : {'required' : True},
            'category': {'required': True},
            'weather': {'required': True},
            'distance': {'required': True},
        }


class RestaurantDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    weather = WeatherSerializer()
    distance = DistanceSerializer()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'category', 'weather',
                  'distance', 'description', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'restaurant', 'content', 'user', 'reg_date', )


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ('id', 'restaurant', 'user', 'rating', )


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('id', 'restaurant', 'user', 'reg_date')


class HistoryDetailSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    user = UserSerializer()

    class Meta:
        model = History
        fields = ('id', 'restaurant', 'user', 'reg_date')