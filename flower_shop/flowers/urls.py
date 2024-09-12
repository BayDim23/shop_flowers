# flowers/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='flowers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='flowers/logout.html'), name='logout'),
    path('', views.flower_catalog, name='flower_catalog'),
    path('order/<int:flower_id>/', views.place_order, name='place_order'),
]
