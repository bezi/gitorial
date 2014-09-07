# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gitorial', '0003_user_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='commit',
        ),
        migrations.RemoveField(
            model_name='line',
            name='src_file',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Line',
        ),
        migrations.RenameField(
            model_name='commit',
            old_name='commit_url',
            new_name='diff_url',
        ),
        migrations.AddField(
            model_name='commit',
            name='files',
            field=jsonfield.fields.JSONField(default=[[]]),
            preserve_default=False,
        ),
    ]
