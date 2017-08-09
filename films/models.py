from django.db import models
from django.forms import ValidationError

import datetime


# Create your models here.

class Zhanr(models.Model):
    name = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50)
    url_name = models.CharField(max_length=50)
    opisanie = models.TextField()
    dlitelnost = models.FloatField()
    format = models.CharField(max_length=3)
    proizvodstvo = models.CharField(max_length=20)
    rezhiser = models.CharField(max_length=50)
    actors = models.TextField()
    year = models.IntegerField()
    image = models.ImageField(
        upload_to="media/films",
        height_field="image_height",
        width_field="image_width"
    )
    image_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        default="525"
    )
    image_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        default="260"
    )
    trailer = models.URLField()
    prokat = models.DateField(blank=True)
    zhanr = models.ManyToManyField(Zhanr)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def zhanr_get(self):
        a = ''
        for i in self.zhanr.all():
            a += i.name + ','

        return a[:-1]


class Seans(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=30)
    film = models.ForeignKey(Film)
    price = models.CommaSeparatedIntegerField(max_length=15)

    def __unicode__(self):
        name = self.film + "," + str(self.date) + " " + str(self.time)
        return name

    def __str__(self):

        name = self.film.name + ", " + str(self.date) + " " + str(self.time)[:5]
        return name

    def film_name_get(self):
        return self.film.name

    def save(self, *args, **kwargs):
        for seans in Seans.objects.filter(date=getattr(self, 'date')):

            time1 = datetime.datetime.combine(
                getattr(self, 'date'),
                datetime.datetime.strptime(
                    getattr(self, 'time'),
                    '%H:%M').time()
            )
            time2 = datetime.datetime.now()

            if getattr(self, 'time') == seans.time or time1 < time2:
                raise ValidationError('Выбрано неподходящее время для сеанса.')

        super(Seans, self).save(*args, **kwargs)


class Bron(models.Model):
    seans_id = models.ForeignKey(Seans)
    forname = models.CharField(max_length=20)
    row = models.IntegerField(default=0)
    seat = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __unicode__(self):
        return self.forname

    def __str__(self):
        return self.forname

    def seans_get(self):
        return self.seans_id.film.name

    def seans_date_get(self):
        return self.seans_id.date

    def seans_time_get(self):
        return self.seans_id.time


class Bilet(models.Model):
    seans_id = models.ForeignKey(Seans)
    row = models.IntegerField(default=0)
    seat = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        sell, created = Sell.objects.get_or_create(seans_id=getattr(self, 'seans_id'))
        sell.kol_bil += 1
        sell.summa += int(getattr(self, 'price'))
        sell.save()

        super(Bilet, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def seans_get(self):
        return self.seans_id.film.name

    def seans_date_get(self):
        return self.seans_id.date

    def seans_time_get(self):
        return self.seans_id.time


class Sell(models.Model):
    seans_id = models.ForeignKey(Seans)
    kol_bil = models.IntegerField(default=0)
    summa = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.seans_id)

    def __str__(self):
        return str(self.seans_id)

    def get_film_name(self):
        return self.seans_id.film.name

    def get_seans_date(self):
        return self.seans_id.date

    def get_seans_time(self):
        return self.seans_id.time
