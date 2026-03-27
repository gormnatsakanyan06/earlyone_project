from django.urls import path
from .views import appointment, finance, government

urlpatterns = [
    path("appointment/", appointment, name="appointment"),
    path('finance/', finance, name='finance'),
    path('government/', government, name='government'),
]