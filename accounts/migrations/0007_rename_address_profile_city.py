# Generated by Django 4.2.6 on 2023-11-14 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_address_line_1_profile_address_line_2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address',
            new_name='city',
        ),
    ]
