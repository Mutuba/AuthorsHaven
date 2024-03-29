# Generated by Django 2.1 on 2018-09-20 12:58

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("description", models.TextField()),
                ("body", models.TextField()),
                (
                    "tagList",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=None,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        max_length=255, null=True, upload_to="myphoto/%Y/%m/%d/"
                    ),
                ),
                ("bookmarked", models.BooleanField(default=False)),
                ("ratings_counter", models.IntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dislike",
                    models.ManyToManyField(
                        blank=True, related_name="dislike", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "like",
                    models.ManyToManyField(
                        blank=True, related_name="like", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ArticleRatings",
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
        migrations.CreateModel(
            name="Comment",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("body", models.TextField()),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="articles.Article",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dislikes",
                    models.ManyToManyField(
                        blank=True, related_name="dislikes", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
