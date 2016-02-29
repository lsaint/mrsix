# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 02:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sixer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.CharField(db_index=True, max_length=16)),
                ('result', models.PositiveIntegerField(default=1)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
