# Generated by Django 4.2.6 on 2023-11-14 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_remove_homeimage_number_homeimage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='setting/')),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField(max_length=1000)),
                ('fb_link', models.URLField()),
                ('twitter_link', models.URLField()),
                ('instagram_link', models.URLField()),
                ('address', models.CharField(max_length=50)),
            ],
        ),
    ]