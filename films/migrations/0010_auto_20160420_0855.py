# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0009_film_prokat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='image',
            field=models.ImageField(height_field='image_height', upload_to='/media/films', width_field='image_width'),
        ),
    ]
