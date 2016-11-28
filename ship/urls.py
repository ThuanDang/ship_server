from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as v
from . import views


router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', v.obtain_auth_token),
    url(r'^search/map/(?P<lat>[0-9]+\.[0-9]{0,9})/(?P<lng>[0-9]+\.[0-9]{0,9})/$', views.search_map)
]
