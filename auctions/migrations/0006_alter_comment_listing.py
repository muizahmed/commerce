# Generated by Django 5.0.1 on 2024-01-19 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_comment_listing_watchlist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="listing",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.listing",
            ),
            preserve_default=False,
        ),
    ]
