from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
  path('', views.home, name='home'),
  path('logout/', views.logout, name='logout'),
  path('login/', views.login, name='login'),
  path('registration/', views.registration, name='registration')
]
