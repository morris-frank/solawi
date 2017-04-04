from django.contrib import admin
from .models import Depot, Product, User, WeeklyBasket, Portion, OrderBasket


class PortionInline(admin.TabularInline):
    ''' '''
    model = Portion
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    ''' '''
    inlines = [PortionInline]


class DepotAdmin(admin.ModelAdmin):
    ''' '''
    pass


class WeeklyBasketAdmin(admin.ModelAdmin):
    ''' '''
    pass


class UserAdmin(admin.ModelAdmin):
    ''' '''
    pass


class OrderBasketAdmin(admin.ModelAdmin):
    ''' '''
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Depot, DepotAdmin)
admin.site.register(WeeklyBasket, WeeklyBasketAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(OrderBasket, OrderBasketAdmin)
