# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0006_tutorial_repo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='index',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
