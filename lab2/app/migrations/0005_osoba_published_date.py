# Generated by Django 5.1.2 on 2024-10-29 10:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_position_alter_coach_age_osoba'),
    ]

    operations = [
        migrations.AddField(
            model_name='osoba',
            name='published_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]