from django.urls import path
from . import new_view, views

urlpatterns = [
    path('', views.home,name="home"),
    
    path('product/<int:productid>', views.product,name="product"),
    path('profile', views.profile,name="profile"),

    path('loginpage', views.loginpage,name="loginpage"),
    path('registeration_page', views.registeration_page,name="registeration_page"),
    path('otp_page', views.otp_page,name="otp_page"),
    path('logout', views.logout,name="logout"),

    path('sell', views.sell,name="sell"),

    path('about', views.about,name="about"),
    
    path('razorpay/', new_view.homepage, name='razorpay'), 
    path('razorpay/paymenthandler/', new_view.paymenthandler, name='paymenthandler'),

]
