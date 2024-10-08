# Generated by Django 4.2.15 on 2024-08-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('unpaid', 'Unpaid')], default='Unpaid', max_length=20),
        ),
    ]
