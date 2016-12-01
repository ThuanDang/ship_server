from django.contrib import admin


# Register your models here.
from ship.models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_url', 'address', 'phone', 'balance')

    def name(self, obj):
        return obj.user.get_full_name()
    name.short_description = 'NAME'

    def user_url(self, obj):
        return '<a href="%s">%s</a>' % ('http://bkship.com/admin/auth/user', obj.user.username)
    user_url.allow_tags = True
    user_url.short_description = 'USERNAME'


class ShipperAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_url', 'address', 'phone', 'balance', 'ratting')

    def name(self, obj):
        return obj.user.get_full_name()
    name.short_description = 'NAME'

    def user_url(self, obj):
        return '<a href="%s">%s</a>' % ('http://bkship.com/admin/auth/user', obj.user.username)
    user_url.allow_tags = True
    user_url.short_description = 'USERNAME'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ship_cost', 'owner', 'shipper', 'status')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude')


class PDLocationAdmin(admin.ModelAdmin):
    list_display = ('location', 'person_name', 'phone')


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'person_name', 'phone')


class CommodityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cost')


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'cost', 'count', 'order')


admin.site.register(Order, OrderAdmin)
admin.site.register(Shipper, ShipperAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(PDLocation, PDLocationAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(CommodityType, CommodityTypeAdmin)
admin.site.register(Commodity, CommodityAdmin)


