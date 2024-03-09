from django.urls import path
from .views import UserApiView,UserLoginApiView,UserLogoutView
urlpatterns = [
    path("user/",UserApiView.as_view(),name="user_api"),
    path("login/",UserLoginApiView.as_view(),name="user_login"),
    path("logout/",UserLogoutView.as_view(),name="logout")
]
