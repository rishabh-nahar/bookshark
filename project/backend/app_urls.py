from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),

    path('product/<int:productid>', views.product,name="product"),
    path('profile', views.profile,name="profile"),

    path('loginpage', views.loginpage,name="loginpage"),
    path('registeration_page', views.registeration_page,name="registeration_page"),
    path('otp_page', views.otp_page,name="otp_page"),

    path('sell', views.sell,name="sell"),
 
    path('about', views.about,name="about"),
]
