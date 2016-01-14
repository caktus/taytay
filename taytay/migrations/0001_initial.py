# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=10)),
                ('producers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=10)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('lyrics', models.TextField()),
                ('writers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=10)),
                ('producers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=10)),
                ('album', models.ForeignKey(to='taytay.Album', on_delete=models.CASCADE)),
            ],
        ),
    ]
