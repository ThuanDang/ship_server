from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.db import models
from rest_framework.authtoken.models import Token


class Account(models.Model):
    """
    Each Customer or Shipper have an Account preference to an User
    """
    user = models.ForeignKey(User)

    # balance
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    # type
    Type_Choice = (
        ('shipper', 'shipper'),
        ('customer', 'customer')
    )
    type = models.CharField(max_length=10, choices=Type_Choice)

    class Meta:
        unique_together = ('user', 'type')

    def send_money(self, receiver, money):
        """
        Send money from an account to another account
        :param receiver: an other account
        :param money: the value of money will be sent
        :return: None if success or raise an Error if fail
        """
        if self.balance >= money:
            self.balance -= money
            receiver.balance += money
        else:
            raise NameError("%s haven't enough money!" % self.user)

    def __str__(self):
        return self.user.username


# -------------------------------------------------------------------------------------


class Customer(models.Model):
    """
    Customer of Shipper, preference to an Account
    """
    account = models.OneToOneField(Account)
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)

    def clean(self):
        if self.account.type == 'shipper':
            raise ValidationError('Account must be a shipper')

    def create_order(self, **kwargs):
        """
        Create new order via primary key and 'orders' relationship
        :param kwargs: attributes of order will be create
        :return:
        """
        self.orders.create(kwargs)

    def update_order(self, pk, **kwargs):
        """
        Update new order via primary key and 'orders' relationship
        :param pk: primary key of order will be update
        :param kwargs: attributes of order
        :return:
        """
        try:
            order = self.orders.get(pk=pk)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            print(e)
        else:
            for key, value in kwargs:
                setattr(order, key, value)
            order.save()

    def delete_order(self, pk):
        """
        Delete order via primary key and 'orders' relationship
        :param pk: primary key of order will be delete
        :return:
        """
        self.orders.get(pk=pk).delete()

    def __str__(self):
        return self.account.user.get_full_name()

# ------------------------------------------------------------------------------------


class Shipper(models.Model):
    """
    Shipper is a person or company that sends or transports goods,
    preference to an Account
    """
    account = models.OneToOneField(Account)
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    card_id = models.CharField(max_length=15, unique=True)
    ratting = models.DecimalField(max_digits=3, decimal_places=2)

    def receive_order(self, pk):
        """
        Receive an order if status of order is 'waiting'
        :param pk: primary key of order
        :return: True of False
        """
        try:
            order = Order.waiting.get(pk=pk)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            print(e)
            return False
        else:
            self.received_orders.add(order)
            return True

# ----------------------------------------------------------------------------------


class WaitingManager(models.Manager):
    """
    Custom filter of Order,
    return Order's objects have status=waiting
    """
    def get_queryset(self):
        return super().get_queryset().filter(status='waiting')


class Type(models.Model):
    """
    Types of Order, consists of attributes:
    - name
    - code
    - cost: Cost of each order type/km
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    cost = models.FloatField()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Orders are created by Customer, include information as:
     name, from_address, to_address, price, ship_cost...
    """
    Status_Choice = (
        ('waiting', 'Waiting'),
        ('not_receive', 'Not Receive'),
        ('received', 'Received'),
        ('complete', 'Complete')
    )

    # information
    name = models.CharField(max_length=50)
    from_address = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='received_location')
    to_address = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_location')
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ship_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # type relationship
    types = models.ManyToManyField(Type, related_name="types")
    # datetime
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # status
    status = models.CharField(max_length=15, choices=Status_Choice, default='waiting')
    # owner and shipper
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    shipper = models.ForeignKey(Shipper, related_name="received_orders", blank=True, null=True)
    # filter
    objects = models.Manager()
    waiting = WaitingManager()

    def __str__(self):
        return self.name














