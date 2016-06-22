from django.db import models

class GuestOtziv(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    text = models.TextField(max_length=20000)
    date = models.DateField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class AdminOtziv(models.Model):
    text = models.TextField(max_length=20000)
    guestOtziv=models.ForeignKey(GuestOtziv)