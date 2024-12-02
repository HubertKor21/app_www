# Generated by Django 5.0.4 on 2024-10-08 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_remove_groups_assigned_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='groups.category'),
        ),
    ]