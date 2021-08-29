from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home_page,name="home"),
    path('chat/',views.chat_page,name='chat'),
    path('chat/send/',views.send_message,name='send_message'),
    path('login/',views.login_page,name="login"),
    path('signup/',views.signup_page,name="signup"),
    path('logout/',views.logout_page,name="logout"),
    path('change_profile_pic/',views.change_profile_pic, name="change_pp"),
    path('create-story/',views.create_story, name="create_story"),

]
