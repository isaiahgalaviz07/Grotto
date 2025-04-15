from django.urls import path
from . import views

urlpatterns = [
    #   Home page
    path('', views.home, name="Home"),
    #   Rooms and room modifiers
    path('room/<str:pk>/', views.room, name="Room"),
    path('profile/<str:pk>/', views.userProfile, name="User Profile"),
    path('create-room/', views.createRoom, name="Create Room"),
    path('update-room/<str:pk>/', views.updateRoom, name="Update Room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="Delete Room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="Delete Message"),
    path('update-user/', views.updateUser, name="Update User"),
    path('topics/', views.topicsPage, name="Topics"),
    path('activity/', views.activityPage, name="Activity"),

    #   User authentication
    path('login/', views.loginPage, name="Login"),
    path('logout/', views.logoutUser, name="Logout"),
    path('register/', views.registerPage, name="Register")
]