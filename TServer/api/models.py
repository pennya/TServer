from django.db import models

# Create your models here.


class Version(models.Model):
    """
    version management
    """
    versionCode = models.IntegerField(default=1)
    versionName = models.CharField(max_length=10, default='1.0.0')
    osType = models.CharField(max_length=10, default='android')

    def __str__(self):
        return self.versionName


class User(models.Model):
    """
    user account management
    """
    u_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.id


class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Weather(models.Model):
    w_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Distance(models.Model):
    d_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    description = models.TextField('DESCRIPTION')

    def __str__(self):
        return self.name


class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_date = models.DateField('REG_DATE',auto_now_add=True)

    def __str__(self):
        return self.restaurant;


class Star(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField('RATING')

    def __str__(self):
        return self.restaurant


class History(models.Model):
    """
    recommand history
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

class RestaurantMap(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=40, null=True)
    longitude = models.CharField(max_length=40, null=True)
    realDistance = models.FloatField(max_length=10, null=True)

class RestaurantImage(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)