from django.contrib import admin
from films.models import *
from django.contrib.admin import DateFieldListFilter
# Register your models here.

@admin.register(Zhanr)
class ZhanrAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Bilet)
class BiletAdmin(admin.ModelAdmin):
    list_display = ('id','seans_get','seans_date_get','seans_time_get','row','seat','price',)
    search_fields = ('seans_id__film__name',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name','proizvodstvo','year','rezhiser','zhanr_get',)
    search_fields = ('name','proizvodstvo','year','rezhiser','zhanr__name')

@admin.register(Seans)
class SeansAdmin(admin.ModelAdmin):
    list_display = ('id','film_name_get','date','time','price',)
    search_fields = ('film__name',)
    list_filter = (
        ('date', DateFieldListFilter),
    )

@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ('forname','seans_get','seans_date_get','seans_time_get','row','seat','price')
    search_fields = ('seans_id__film__name','forname',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )

@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ('get_film_name','get_seans_date','get_seans_time','kol_bil','summa',)
    search_fields = ('seans_id__film__name','seans_id__date',)
    list_filter = (
        ('seans_id__date', DateFieldListFilter),
    )

