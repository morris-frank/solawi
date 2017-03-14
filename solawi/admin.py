from django.contrib import admin
from .models import Depot, Food, Portion, TimedPortions, User, WeeklyBasket


class FoodAdmin(admin.ModelAdmin):
    pass


class DepotAdmin(admin.ModelAdmin):
    pass


class WeeklyBasketAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Food, FoodAdmin)
admin.site.register(Depot, DepotAdmin)
admin.site.register(WeeklyBasket, WeeklyBasketAdmin)
admin.site.register(User, UserAdmin)
