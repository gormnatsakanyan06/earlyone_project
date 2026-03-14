from django.contrib import admin
from django.urls import path
from django.urls import path, include


from core.views import *



urlpatterns = [
    path('', home),   # homepage
    path('admin/', admin.site.urls),
    path("chaining/", include("smart_selects.urls")),

    path('banks/', banks),
    path('banks/branches/', bank_branches),
    path('banks/actions/', bank_actions),

    path('services/',service),
    path('services/branches/',service_branches),
    path('services/actions/',service_actions),

    path('telecom/',telecom),
    path('telecom/branches/',telecom_branches),
    path('telecom/actions/',telecom_actions),

    path('government/',government),
    path('government/branches/',government_actions),
    path('government/actions/',government_actions)
]