from django.urls import path
from ashaease import views

urlpatterns = [
    path('',views.base, name="base"),
    path('register', views.register, name="register"),
]