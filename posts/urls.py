from django.urls import path,include

from . import views

app_name="posts"

urlpatterns = [
    path('', views.post_comment_create_list_view,name='all'),
    path("like-unlike/",views.like_unlike_post,name="like_unlike_post"),
    path("remove/<str:pk>/",views.remove,name="remove"),
    path("update/<str:pk>/",views.update,name="update"),
    path("search",views.search_method,name="search")
]
