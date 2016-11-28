
from rest_framework import serializers

from ship.models import Order, Customer, Shipper


class OwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone', 'address')

    @staticmethod
    def get_full_name(obj):
        return obj.account.user.get_full_name()


class OrderSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'from_address', 'to_address', 'description',
                  'price', 'ship_cost', 'status', 'types', 'owner')
        depth = 1
        read_only_fields = ('shipper', 'status')


class ShipperSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_full_name')
    email = serializers.SerializerMethodField('get_email')

    class Meta:
        model = Shipper
        fields = ('id', 'name', 'address', 'phone', 'email', 'received_orders')

    @staticmethod
    def get_email(obj):
        return obj.account.user.email

    @staticmethod
    def get_full_name(obj):
        return obj.account.user.get_full_name()