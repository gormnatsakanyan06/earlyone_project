from django.contrib import admin
from .models import Category, Provider, Branch, Action, QRCode, Appointment

# This allows you to add Branches while editing a Provider
class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1 
    prepopulated_fields = {"slug": ("name",)}

# This allows you to add Actions while editing a Provider
class ActionInline(admin.TabularInline):
    model = Action
    extra = 1
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}
    # Add the inlines here
    inlines = [BranchInline, ActionInline]

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'city', 'address')
    list_filter = ('provider', 'city')
    search_fields = ('name', 'address')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider')
    list_filter = ('provider',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'status', 'scheduled_at')
    list_filter = ('status', 'category')
    readonly_fields = ('verification_code', 'created_at')

admin.site.register(QRCode)