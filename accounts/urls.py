from django.urls import path

from .views import (HomeView,SignupView,UserLoginView,UserLogoutView,)


urlpatterns = [

    path("",HomeView.as_view(),name="home"),
    path("signup/",SignupView.as_view(),name="signup"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    
]