# Generated by Django 5.0.4 on 2024-11-06 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_invite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='family',
            name='members',
        ),
        migrations.RemoveField(
            model_name='invite',
            name='invited_by',
        ),
    ]