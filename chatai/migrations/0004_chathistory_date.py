# Generated by Django 4.1.7 on 2023-03-20 19:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatai", "0003_alter_chathistory_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="chathistory",
            name="Date",
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
