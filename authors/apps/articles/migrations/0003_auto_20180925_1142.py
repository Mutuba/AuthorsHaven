# Generated by Django 2.1 on 2018-09-25 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0002_report"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleRating",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.TextField()),
                ("rating", models.IntegerField()),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articlerating",
                        to="articles.Article",
                    ),
                ),
                (
                    "rater",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articlesrating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="articleratings",
            name="article",
        ),
        migrations.RemoveField(
            model_name="articleratings",
            name="rater",
        ),
        migrations.DeleteModel(
            name="ArticleRatings",
        ),
    ]
