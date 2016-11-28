from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ship.models import Order
from ship.permissions import IsOwnerOrReadOnly
from ship.serializers import OrderSerializer
from ship.utils import get_orders_nearest


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.waiting.all().order_by('created')
    serializer_class = OrderSerializer

    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.account.customer)


@api_view(['GET'])
def received_order(request, pk):
    if request.user.account.shipper.received_orders(pk):
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_map(request, lat, lng):
    orders = Order.waiting.all()
    data = get_orders_nearest(float(lat), float(lng), orders)

    serializer = OrderSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)







