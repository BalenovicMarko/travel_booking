# Generated by Django 5.1.3 on 2024-12-23 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_reservation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='total_price',
        ),
    ]
