from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This connects your project to the core app's URLs
    path('', include('core.urls')), 
]