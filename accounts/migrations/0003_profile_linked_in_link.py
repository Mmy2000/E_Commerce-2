# Generated by Django 4.2.6 on 2023-10-31 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_about_profile_fb_link_profile_instagram_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linked_in_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
