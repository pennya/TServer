from django.db import models

# Create your models here.


"""
버전 관리
"""
class Version(models.Model):
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.version



"""
사용자 계정 관리
"""
class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.id


"""
카테고리
"""
class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

"""
날씨
"""
class Weather(models.Model):
    w_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
"""
거리
"""
class Distance(models.Model):
    d_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
"""
음식점
"""
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    description = models.TextField('DESCRIPTION')

    def __str__(self):
        return self.name

"""
댓글
"""
class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_date = models.DateField('REG_DATE',auto_now_add=True)

    def __str__(self):
        return self.restaurant;

"""
별점
"""
class Star(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField('RATING')

    def __str__(self):
        return self.comment

"""
추천이력
"""
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user
