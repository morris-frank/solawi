from django.contrib import admin
from .models import Depot, Product, User, WeeklyBasket, Portion


class ProductAdmin(admin.ModelAdmin):
    pass


class DepotAdmin(admin.ModelAdmin):
    pass


class WeeklyBasketAdmin(admin.ModelAdmin):
    pass


class PortionAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Depot, DepotAdmin)
admin.site.register(WeeklyBasket, WeeklyBasketAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(User, UserAdmin)
