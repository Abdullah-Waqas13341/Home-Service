# Generated by Django 4.2.15 on 2024-08-25 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_booking_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='booking',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='customers.booking'),
        ),
    ]
