# Generated by Django 4.0.6 on 2022-07-16 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
