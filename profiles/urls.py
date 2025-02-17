from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order__history/<order_number>',
         views.order_history, name='order_history'),
]
