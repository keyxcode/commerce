# Generated by Django 4.0.6 on 2022-07-16 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='url',
            new_name='image_url',
        ),
    ]