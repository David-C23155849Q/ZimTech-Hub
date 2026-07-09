from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/edit/', views.ProfileUpdateView.as_view(), name='edit'),
    path('top/', views.TopProfilesView.as_view(), name='top'),
]
