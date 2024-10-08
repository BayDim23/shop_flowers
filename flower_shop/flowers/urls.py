from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.flower_catalog, name='flower_catalog'),
    path('order/<int:flower_id>/', views.place_order, name='place_order'),
]
