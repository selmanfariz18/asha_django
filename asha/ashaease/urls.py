from django.urls import path
from ashaease import views

urlpatterns = [
    path('',views.base, name="base"),
    path('register', views.register, name="register"),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name="home"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
]