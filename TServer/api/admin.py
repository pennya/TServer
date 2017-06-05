from django.contrib import admin

# Register your models here.
from api.models import *


class VersionAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class WeatherAdmin(admin.ModelAdmin):
    pass

class DistanceAdmin(admin.ModelAdmin):
    pass

class RestaurantAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class StarAdmin(admin.ModelAdmin):
    pass

class HistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Version, VersionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Weather, WeatherAdmin)
admin.site.register(Distance, DistanceAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Star, StarAdmin)
admin.site.register(History, HistoryAdmin)