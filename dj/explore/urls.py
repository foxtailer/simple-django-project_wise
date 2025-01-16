from django.urls import path

from explore import views


app_name = 'explore'

urlpatterns = [
  path('', views.explore, name='explore'),
  path('report/', views.report, name='report'),
]
