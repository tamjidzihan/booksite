from django.urls import path
from . import views;


urlpatterns = [
    path('',views.index,name="index"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="registerPage"),
    path('logout/', views.logout, name="logout"),
    path('postsign/', views.postsignin, name="postsignin"),
]