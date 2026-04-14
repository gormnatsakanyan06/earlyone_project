from django.urls import path, include # Add include here
from . import views

urlpatterns = [
    # Allauth system paths (Required for Google login to work)
    path('accounts/', include('allauth.urls')),

    # Your existing paths
    path('', views.appointment_landing_view, name='appointment_landing' ),
    path('appointment/', views.appointment_landing_view, name='appointment_landing'),

    path('<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('<slug:category_slug>/<slug:provider_slug>/', views.branch_list_view, name='branch_list'),
    path('<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/', views.action_list_view, name='action_list'),
]