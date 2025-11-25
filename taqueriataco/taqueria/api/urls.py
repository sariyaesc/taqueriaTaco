from django.urls import path
from .views import ProductListAPI, OrderListCreateAPI

urlpatterns = [
    path('tacos/', ProductListAPI.as_view(), name='api-tacos'),
    path('orders/', OrderListCreateAPI.as_view(), name='api-orders'),
]
