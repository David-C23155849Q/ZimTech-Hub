"""
Jobs API URL patterns.
"""
from django.urls import path
from . import views

app_name = "jobs_api"

urlpatterns = [
    path('', views.job_list, name='job_list'),
]
