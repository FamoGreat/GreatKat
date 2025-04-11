from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('increment/<int:cart_item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]