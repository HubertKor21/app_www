# Generated by Django 5.0.4 on 2024-11-15 15:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invitations', '0005_alter_family_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount_reaming', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Kwota pozostała do spłaty')),
                ('loan_type', models.CharField(choices=[('fixed', 'Stałe'), ('decreasing', 'Malejące')], default='fixed', max_length=10, verbose_name='Rodzaj rat')),
                ('interest_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Oprocentowanie')),
                ('payment_day', models.PositiveSmallIntegerField(verbose_name='Dzień płatności raty')),
                ('last_payment_date', models.DateField(verbose_name='Data spłaty ostatniej raty')),
                ('installments_remaining', models.PositiveIntegerField(verbose_name='Pozostało rat')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='invitations.family')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Kredyt',
                'verbose_name_plural': 'Kredyty',
            },
        ),
    ]
