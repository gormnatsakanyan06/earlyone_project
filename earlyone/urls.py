from django.contrib import admin
from django.urls import path, include

from core.views import *
from core.qr import create_qr, download_qr

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path("chaining/", include("smart_selects.urls")),

    # Banks
    path('banks/', banks),
    path('banks/branches/', bank_branches),
    path('banks/actions/', bank_actions),

    # Services
    path('services/', service),
    path('services/branches/', service_branches),
    path('services/actions/', service_actions),

    # Telecom
    path('telecom/', telecom),
    path('telecom/branches/', telecom_branches),
    path('telecom/actions/', telecom_actions),

    # Government
    path('government/', government),
    path('government/branches/', government_branches),
    path('government/actions/', government_actions),

    #  QR
    path('qr/', create_qr),
    path('qr/<int:qr_id>/download/', download_qr),
    # core/urls.py
    path('appointment', appointment),
    path('book-appointment/',create_appointment, name='create_appointment'),
    path('', include('core.urls')),
]

# ✅ IMPORTANT: use += NOT =
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)