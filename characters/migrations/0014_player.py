# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 04:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('characters', '0013_auto_20161212_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('level', models.IntegerField(default=1)),
                ('alignment', models.CharField(choices=[('Unaligned', 'Unaligned'), ('LG', 'Lawful Good'), ('NG', 'Neutral Good'), ('CG', 'Chaotic Good'), ('LN', 'Lawful Neutral'), ('N', 'Neutral'), ('CN', 'Chaotic Neutral'), ('LE', 'Lawful Evil'), ('NE', 'Neutral Evil'), ('CE', 'Chaotic Evil')], default='Neutral', max_length=255)),
                ('size', models.CharField(choices=[('Tiny', 'Tiny'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Huge', 'Huge'), ('Gargantuan', 'Gargantuan')], default='Medium', max_length=255)),
                ('languages', models.CharField(blank=True, max_length=255)),
                ('strength', models.IntegerField(blank=True, default=10)),
                ('dexterity', models.IntegerField(blank=True, default=10)),
                ('constitution', models.IntegerField(blank=True, default=10)),
                ('intelligence', models.IntegerField(blank=True, default=10)),
                ('wisdom', models.IntegerField(blank=True, default=10)),
                ('charisma', models.IntegerField(blank=True, default=10)),
                ('armor_class', models.IntegerField(blank=True, default=0)),
                ('hit_points', models.CharField(blank=True, max_length=255)),
                ('speed', models.CharField(blank=True, default='', max_length=255)),
                ('saving_throws', models.CharField(blank=True, default='', max_length=255)),
                ('skills', models.CharField(blank=True, default='', max_length=255)),
                ('initiative', models.CharField(blank=True, default='', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
