# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('commit_url', models.CharField(max_length=100)),
                ('code_url', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('commit', models.ForeignKey(to='gitorial.Commit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('content', models.CharField(max_length=200)),
                ('addition', models.BooleanField()),
                ('deletion', models.BooleanField()),
                ('src_file', models.ForeignKey(to='gitorial.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content_before', models.CharField(max_length=500)),
                ('content_after', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('repo_url', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(primary_key=True, max_length=50, serialize=False)),
                ('avatar_url', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='owner',
            field=models.ForeignKey(to='gitorial.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='tutorial',
            field=models.ForeignKey(to='gitorial.Tutorial'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commit',
            name='step',
            field=models.OneToOneField(to='gitorial.Step'),
            preserve_default=True,
        ),
    ]
