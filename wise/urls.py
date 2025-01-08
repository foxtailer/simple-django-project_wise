from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('explore/', include('explore.urls', namespace='explore')),
    path('book/', include('book.urls', namespace='book')),
    path('write/', include('write.urls', namespace='write')),
]
