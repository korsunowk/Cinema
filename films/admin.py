from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from films.models import *


# Register your models here.

@admin.register(Zhanr)
class ZhanrAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Bilet)
class BiletAdmin(admin.ModelAdmin):
    list_display = ('id', 'seans_get', 'seans_date_get', 'seans_time_get', 'row', 'seat', 'price',)
    search_fields = ('seans_id__film__name',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'proizvodstvo', 'year', 'rezhiser', 'zhanr_get',)
    search_fields = ('name', 'proizvodstvo', 'year', 'rezhiser', 'zhanr__name')


@admin.register(Seans)
class SeansAdmin(admin.ModelAdmin):
    list_display = ('id', 'film', 'date', 'time', 'price',)
    search_fields = ('film__name',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    fieldsets = ((
        None, {
            'fields': ('date', 'time', 'film', 'price')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "film":
            kwargs["queryset"] = Film.objects.filter(prokat__lte=datetime.datetime.today().date())
        return super(SeansAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ('forname', 'seans_get', 'seans_date_get', 'seans_time_get', 'row', 'seat', 'price')
    search_fields = ('seans_id__film__name', 'forname',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )


@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ('get_film_name', 'get_seans_date', 'get_seans_time', 'kol_bil', 'summa',)
    search_fields = ('seans_id__film__name', 'seans_id__date',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )
