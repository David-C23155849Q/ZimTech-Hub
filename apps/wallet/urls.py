from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.WalletView.as_view(), name='index'),
]
