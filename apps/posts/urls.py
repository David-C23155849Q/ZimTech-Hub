from django.urls import path
from . import views

app_name = "posts"


urlpatterns = [

    path(
        "",
        views.FeedView.as_view(),
        name="feed"
    ),

    path(
        "create/",
        views.PostCreateView.as_view(),
        name="create"
    ),

    path(
        "<uuid:pk>/",
        views.PostDetailView.as_view(),
        name="detail"
    ),

]