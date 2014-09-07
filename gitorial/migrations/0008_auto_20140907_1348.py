# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0007_step_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='code_url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='step',
            name='content_after',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='step',
            name='content_before',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='step',
            name='diff_url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='description',
            field=models.TextField(),
        ),
    ]
