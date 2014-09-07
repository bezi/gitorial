# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0005_auto_20140907_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='repo_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
