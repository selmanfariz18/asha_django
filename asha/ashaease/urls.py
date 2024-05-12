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
    path('notification', views.notification, name="notification"),
    path('report/', views.report, name='report'),
    path('report_edit', views.report_edit, name='report_edit'),
    path('report_edit_maintain', views.report_edit_maintain, name='report_edit_maintain'),
    path('report_view', views.report_view, name='report_view'),
    path('report_delete', views.report_delete, name='report_delete'),
    path('house_hold', views.house_hold, name='house_hold'),
    path('children', views.children, name='children'),
    path('pregnant', views.pregnant, name='pregnant'),    
]