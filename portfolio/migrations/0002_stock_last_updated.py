# Generated by Django 5.0.7 on 2024-12-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
