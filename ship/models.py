from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from rest_framework.authtoken.models import Token


class Location(models.Model):
    address = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address


class PDLocation(models.Model):
    person_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    location = models.ForeignKey(Location)

    class Meta:
        verbose_name = 'PD Location'
        verbose_name_plural = 'PD Locations'

    def __str__(self):
        return self.location.address


class Customer(models.Model):
    """
    Customer of Shipper, preference to an User
    """
    user = models.OneToOneField(User)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def create_order(self, **kwargs):
        self.orders.create(kwargs)

    def update_order(self, pk, **kwargs):
        try:
            order = self.orders.get(pk=pk)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            print(e)
        else:
            for key, value in kwargs:
                setattr(order, key, value)
            order.save()

    def delete_order(self, pk):
        self.orders.get(pk=pk).delete()

    def __str__(self):
        return self.user.get_full_name()


class Warehouse(PDLocation):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Customer, related_name='warehouses')

    def __str__(self):
        return '{0}-{1}'.format(self.name, self.address)


class Shipper(models.Model):
    """
    Shipper is a person or company that sends or transports goods,
    preference to an Account
    """
    user = models.OneToOneField(User)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    card_id = models.CharField(max_length=15, unique=True)
    ratting = models.DecimalField(max_digits=3, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location)

    def receive_order(self, pk):
        try:
            order = Order.waiting.get(pk=pk)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            print(e)
            return False
        else:
            self.my_received_orders.add(order)
            return True

    def __str__(self):
        return self.user.get_full_name()


class WaitingManager(models.Manager):
    """
    Custom filter of Order,
    return Order's objects have status=waiting
    """
    def get_queryset(self):
        return super().get_queryset().filter(status='waiting')


class Order(models.Model):
    """
    Orders are created by Customer, include information as:
     name, from_address, to_address, price, ship_cost...
    """
    Status_Choice = (
        ('waiting', 'waiting'),
        ('received', 'received'),
        ('picked up', 'picked up'),
        ('delivered', 'delivered'),
        ('completed', 'completed')
    )

    Types_Choice = (
        (1, 'paid'),
        (2, 'unpaid')
    )

    # information
    name = models.CharField(max_length=50)
    from_address = models.ForeignKey(PDLocation, on_delete=models.CASCADE, related_name='pickup_location')
    to_address = models.ForeignKey(PDLocation, on_delete=models.CASCADE, related_name='delivery_location')
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ship_cost = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.IntegerField(choices=Types_Choice)
    # datetime
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # status
    status = models.CharField(max_length=15, choices=Status_Choice, default='waiting')
    # owner and shipper
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='my_orders')
    shipper = models.ForeignKey(Shipper, related_name="my_received_orders", blank=True, null=True)
    # filter
    objects = models.Manager()
    waiting = WaitingManager()

    def __str__(self):
        return self.name


class CommodityType(models.Model):
    """
    Type of Commodity, example: phone, computer, clothes...
    - cost: transportation cost of each commodity type/km, purpose for suggest to Customer
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Commodity(models.Model):
    """
    An Order can include many Commodity
    cost: transportation cost is given by Customer
    """
    name = models.CharField(max_length=50)
    type = models.ForeignKey(CommodityType, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    order = models.ForeignKey(Order, related_name='commodities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'commodities'














