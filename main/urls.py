from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
  path('', views.home, name='home'),
  path('write/', views.write, name='write'),
  path('explore/', views.explore, name='explore'),
  path('my/', views.my, name='my'),
  path('logout/', views.logout, name='logout'),
  path('report/', views.report, name='report'),
  path('login/', views.login, name='login'),
  path('registration/', views.registration, name='registration')
]