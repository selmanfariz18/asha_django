from django.urls import path
from ashaease import views

urlpatterns = [
    path('',views.base, name="base"),
    path('register', views.register, name="register"),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name="home"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('change_password', views.change_password, name="change_password"),
    path('calendar/', views.calendar, name="calendar"),
    path('events/<int:year>/<int:month>/<int:day>/', views.get_events_by_day, name='get_events_by_day'),  
    path('events/<int:year>/<int:month>/', views.get_events, name='get_events'),  
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
]