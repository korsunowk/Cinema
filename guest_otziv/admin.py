from django.contrib import admin
from guest_otziv.models import GuestOtziv,AdminOtziv
from django.contrib.admin import DateFieldListFilter

@admin.register(GuestOtziv)
class GuestOtzivAdmin(admin.ModelAdmin):
    list_display = ('name','email','date')
    search_fields = ('name',)
    list_filter = (
        ('date', DateFieldListFilter),
    )

@admin.register(AdminOtziv)
class AdminOtzivAdmin(admin.ModelAdmin):
    list_display = ('guestOtziv','text',)
    search_fields = ('guestOtziv__name',)
    list_filter = (
        ('guestOtziv__date', DateFieldListFilter),
    )