from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('signin/', views.signin_view, name='signin'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.cart_add, name='cart-add'),
    path('cart/update/', views.cart_update, name='cart-update'),
    path('cart/remove/', views.cart_remove, name='cart-remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_view, name='success'),
    path('api/', include('taqueria.api.urls')),
]
