"""ProjectBoon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from boonapp import views
urlpatterns = [
    path('home/',views.home,name="home"),
    path('', views.login, name="login"),
    path('home/get-inbox/',views.get_inbox,name="get_inbox"),
    path('home/get-contacts/', views.get_contacts, name="get_contacts"),
    path('home/get-settings/',views.get_settings,name="get_settings"),
    path('chat/<int:id>/<int:friend>/',views.chat,name='chat'),
    path('chat/<int:id>/<int:friend>/send-message/',views.sendMessage,name='send-message'),
    path('add-contact/<int:id>/',views.save_contact_from_id,name="add-contact"),
    path('add-contact-email/',views.save_contact_from_email,name="add-contact"),
    path('get_remained_msg/',views.get_remained_msg),
    path('home/change-dp/',views.change_dp)

]
