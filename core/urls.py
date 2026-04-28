from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [ 
    path('accounts/', include('allauth.urls')),
     # appointment
    path('', views.appointment_landing_view, name='appointment_landing'),
    path('appointment/', views.appointment_landing_view, name='appointment_landing'),
     # api
    path('api/create-appointment/', views.create_appointment, name='create_appointment'),
     # ticket
    path('ticket/<int:appointment_id>/', views.ticket_view, name='ticket'),
    # datetime
    path(
        '<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/datetime/<str:hash>/',
        views.datetime_view,
        name="datetime"
    ),
    path('<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('<slug:category_slug>/<slug:provider_slug>/', views.branch_list_view, name='branch_list'),
    path('<slug:category_slug>/<slug:provider_slug>/<slug:branch_slug>/actions/', views.action_list_view, name='action_list'),
]

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)