from django.contrib import admin
from .models import (
    Service, ServiceBranch, ServiceAction,
    Telecom, TelecomBranch, TelecomAction,
    Government, GovernmentBranch, GovernmentAction,
    Bank, BankBranch, BankAction,QRCode
)
from django.utils.html import format_html
# Register all models
admin.site.register(Service)
admin.site.register(ServiceBranch)
admin.site.register(ServiceAction)

admin.site.register(Telecom)
admin.site.register(TelecomBranch)
admin.site.register(TelecomAction)

admin.site.register(Government)
admin.site.register(GovernmentBranch)
admin.site.register(GovernmentAction)

admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(BankAction)




@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'qr_preview', 'created_at')

    def qr_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.image.url
            )
        return "No Image"

    qr_preview.short_description = "QR Code"