# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0002_auto_20140906_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_updated',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
