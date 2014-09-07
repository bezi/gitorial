# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0009_auto_20140907_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='files',
            field=jsonfield.fields.JSONField(),
        ),
    ]
