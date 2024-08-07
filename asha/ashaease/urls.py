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
    path('delete_event', views.delete_event, name='delete_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('notification', views.notification, name="notification"),
    path('report/', views.report, name='report'),
    path('report_edit', views.report_edit, name='report_edit'),
    path('report_edit_maintain', views.report_edit_maintain, name='report_edit_maintain'),
    path('report_view', views.report_view, name='report_view'),
    path('report_delete', views.report_delete, name='report_delete'),
    path('house_hold', views.house_hold, name='house_hold'),
    path('search_house_hold', views.search_house_hold, name='search_house_hold'),
    path('add_member', views.add_member, name='add_member'),
    path('add_member_request', views.add_member_request, name='add_member_request'),
    path('house_details', views.house_details, name='house_details'),
    path('children', views.children, name='children'),
    path('search_children', views.search_children, name='search_children'),
    path('add_children_request', views.add_children_request, name='add_children_request'),
    path('add_children', views.add_children, name='add_children'),
    path('pregnant', views.pregnant, name='pregnant'),
    path('search_pregnant', views.search_pregnant, name='search_pregnant'),
    path('add_pregnant_request', views.add_pregnant_request, name='add_pregnant_request'),
    path('add_pregnant', views.add_pregnant, name='add_pregnant'),
    path('patient', views.patient, name='patient'),
    path('search_patient', views.search_patient, name='search_patient'),      
    path('add_patient_request', views.add_patient_request, name='add_patient_request'),    
    path('add_patient', views.add_patient, name='add_patient'),    
    path('edit_household', views.edit_household, name='edit_household'),
    path('edit_pregnant', views.edit_pregnant, name='edit_pregnant'),
    path('edit_patient', views.edit_patient, name='edit_patient'),
    path('edit_children', views.edit_children, name='edit_children'),
]