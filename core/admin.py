from django.contrib import admin
from .models import (
    Service, ServiceBranch, ServiceAction,
    Telecom, TelecomBranch, TelecomAction,
    Government, GovernmentBranch, GovernmentAction,
    Bank, BankBranch, BankAction
)

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