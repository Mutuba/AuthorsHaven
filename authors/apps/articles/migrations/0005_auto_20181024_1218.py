# Generated by Django 2.1 on 2018-10-24 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_auto_20181024_1024"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
