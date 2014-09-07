# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0008_auto_20140907_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='files',
            field=models.TextField(),
        ),
    ]
