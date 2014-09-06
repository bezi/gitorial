# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='addition',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='line',
            name='deletion',
            field=models.BooleanField(default=False),
        ),
    ]
