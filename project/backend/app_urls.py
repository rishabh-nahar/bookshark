from django.urls import path
from . import new_view, views

urlpatterns = [
    path('', views.home,name="home"),
    
    path('product/<int:productid>', views.product,name="product"),

    path('my_orders', views.my_orders,name="my_orders"),
    path('profile', views.profile,name="profile"),
    path('edit_profile', views.edit_profile,name="edit_profile"),

    path('loginpage', views.loginpage,name="loginpage"),
    path('registeration_page', views.registeration_page,name="registeration_page"),
    path('otp_page', views.otp_page,name="otp_page"),
    path('send_mail', views.send_mail,name="send_mail"),
    path('logout', views.logout,name="logout"),

    path('sell', views.sell,name="sell"),

    path('about', views.about,name="about"),
    
    path('product/<int:productid>/paymenthandler/<int:amount>', views.paymenthandler, name='paymenthandler'),

]
