# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taytay.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taytay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(default=taytay.models.slug, max_length=32, unique=True)),
                ('lyrics', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
