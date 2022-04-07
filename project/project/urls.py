from django.contrib import admin
from django.urls import path,include
# import backend 

urlpatterns = [
    path('',include('backend.app_urls')),
    path('admin/', admin.site.urls),
]