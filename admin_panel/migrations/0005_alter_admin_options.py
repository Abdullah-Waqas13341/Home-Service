# Generated by Django 4.2.15 on 2024-08-14 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_delete_admin_admin_alter_adminaction_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'verbose_name': 'Admin', 'verbose_name_plural': 'Admins'},
        ),
    ]
