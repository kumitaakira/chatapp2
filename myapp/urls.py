from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView



urlpatterns = [
    path('signup',views.AccountRegistration.as_view(), name='signup'),
    path('',views.index,name='index'),
    path('login',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path("friends",views.home,name="home"),
    path("talk_room",views.talk_room,name="talk_room"),
    path('setting',views.setting,name='setting'),
    path('talk_room_back',views.talk_room_back,name='talk_room_back'),
    path('message/',views.message,name='message'),
    path('message/<str:sender>',views.message,name='message'),
    path('change',views.change,name='change'),
    path('password',PasswordChangeView.as_view(success_url='complete'),name='password'),
    path('complete',views.complete,name='complete'),
    ]

