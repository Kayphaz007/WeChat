from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('room/<int:pk>', views.rooms, name='room'),
    
    
    path('room_form/', views.room_form, name='create_room'),
    path('update_room/<int:pk>', views.updateRoom, name='update_room'),
    path('delete_room/<int:pk>', views.deleteRoom, name='delete_room'),
    
    path('userProfile/<str:pk>', views.userProfile, name='userProfile'),
    path('updateUser/', views.updateUser, name='updateUser'),
    
    path('delete_comment/<int:pk>', views.deleteComment, name='delete_comment'),
    
    path('topics/', views.topicsPage, name='topicsPage'),
    path('activities/', views.activityPage, name='activitiesPage'),
    
    path('login_page/', views.loginPage, name='loginPage'),
    path('reg_user/', views.registerUser, name='regUser'),
    path('logout_page/', views.logoutPage, name='logoutPage'),
]