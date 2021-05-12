from django.urls import path
from . import views

urlpatterns = [
    path('scrapper/', views.scrapper, name="scrapper"),
    path('get_eth_price/', views.get_eth_price, name="get_eth_price"),
    path('get_eth_amount_in_an_address/', views.get_eth_amount_in_an_address, name="get_eth_amount_in_an_address")
]
