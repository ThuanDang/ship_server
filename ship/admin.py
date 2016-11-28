from django.contrib import admin


# Register your models here.
from ship.forms import CustomerAdminForm, ShipperAdminForm
from ship.models import Order, Type, Customer, Shipper, Account, Location


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_url', 'balance', 'type')

    def user_url(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://bkship.com/admin/auth/account/', obj.user.id, obj.user.username)

    user_url.allow_tags = True
    user_url.short_description = 'account'


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ('id', 'name', 'account_url', 'phone', 'address')

    def name(self, obj):
        return obj.account.user.get_full_name()

    name.short_description = 'NAME'

    def account_url(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://bkship.com/admin/ship/account/', obj.account.id, obj.account)

    account_url.allow_tags = True
    account_url.short_description = 'ACCOUNT'


class ShipperAdmin(admin.ModelAdmin):
    form = ShipperAdminForm
    list_display = ('id', 'name', 'account_url', 'phone', 'ratting', 'address')

    def name(self, obj):
        return obj.account.user.get_full_name()

    name.short_description = 'NAME'

    def account_url(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://bkship.com/admin/ship/account/', obj.account.id, obj.account)

    account_url.allow_tags = True
    account_url.short_description = 'ACCOUNT'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ship_cost', 'owner', 'shipper', 'status')
    filter_horizontal = 'types',


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cost')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


admin.site.register(Order, OrderAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Shipper, ShipperAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Location, LocationAdmin)
