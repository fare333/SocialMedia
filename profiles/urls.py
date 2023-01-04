from django.urls import path,include

from . import views
from .views import ProfileListView
app_name = "profiles"

urlpatterns = [
    path("myprofile/",views.my_profile,name="get_my_profile"),
    path("my-invites",views.invites_received_views,name="my_invites"),
    path("profile-list",ProfileListView.as_view(),name="profile_list"),
    path("invite-profile-list",views.invite_profile_list_views,name="invite_profile_list"),
    path("profile-details/<str:slug>/",views.get_profile_detail,name="get_profile_detail"),
    path("invitation",views.sent_invitation,name="sent_invitation"),
    path("remove_from_friends",views.remove_from_friend,name="remove_from_friend"),
    path("my-invites/reject/",views.reject_invitation,name="reject_invitation"),
    path("my-invites/accept/",views.accept_invitation,name="accept_invitation"),
    path("login",views.sign_in,name="login"),
    path("logout",views.sign_out,name="logout"),
    path("register",views.register,name="register")
]
