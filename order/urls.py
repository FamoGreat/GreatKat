from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('mock_payment/', views.mock_payment, name='mock_payment'),
    path('order_complete/', views.order_complete, name='order_complete'),
]