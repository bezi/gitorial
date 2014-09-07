# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0004_auto_20140907_0235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='step',
        ),
        migrations.DeleteModel(
            name='Commit',
        ),
        migrations.AddField(
            model_name='step',
            name='code_url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='step',
            name='diff_url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='step',
            name='files',
            field=jsonfield.fields.JSONField(default=[[]]),
            preserve_default=False,
        ),
    ]
