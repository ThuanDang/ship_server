
from rest_framework import serializers

from ship.models import Order, Customer, Shipper


class OwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone', 'address')

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class OrderSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'from_address', 'to_address', 'description',
                  'price', 'ship_cost', 'status', 'type', 'owner', 'commodities')
        depth = 2
        read_only_fields = ('shipper', 'status')


class ShipperSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_full_name')
    email = serializers.SerializerMethodField('get_email')

    class Meta:
        model = Shipper
        fields = ('id', 'name', 'address', 'phone', 'email', 'ratting', 'balance')

    def get_email(self, obj):
        return obj.user.email

    def get_full_name(self, obj):
        return obj.user.get_full_name()
