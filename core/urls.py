from django.urls import path, include # Add include here
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),

    path('', views.appointment_landing_view, name='appointment_landing'),
    path('appointment/', views.appointment_landing_view, name='appointment_landing'),

    # ✅ ADD THESE BEFORE slug
    # path('datetime/', views.datetime_view, name='datetime'),
    path('api/create-appointment/', views.create_appointment, name='create_appointment'),
    # path('<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/datetime/<str:hash>/',views.datetime_view,name="datetime"),
    path(
    '<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/datetime/<str:hash>/',
    views.datetime_view,
    name="datetime"
),

    # existing
    path('<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('<slug:category_slug>/<slug:provider_slug>/', views.branch_list_view, name='branch_list'),
    path('<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/', views.action_list_view, name='action_list'),
    
]

