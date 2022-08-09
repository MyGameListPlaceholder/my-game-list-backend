# Generated by Django 4.0.6 on 2022-08-09 17:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Developer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
            ],
            options={
                "verbose_name": "developer",
                "verbose_name_plural": "developers",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True, verbose_name="title")),
                (
                    "creation_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="last modified"),
                ),
                (
                    "release_date",
                    models.DateField(blank=True, null=True, verbose_name="release date"),
                ),
                (
                    "cover_image",
                    models.ImageField(upload_to="cover_images/", verbose_name="cover image"),
                ),
                ("description", models.TextField(blank=True, verbose_name="description")),
            ],
            options={
                "verbose_name": "game",
                "verbose_name_plural": "games",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GameFollow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "creation_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
                ),
            ],
            options={
                "verbose_name": "game follow",
                "verbose_name_plural": "games followed",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GameList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Completed"),
                            ("PTP", "Plan to play"),
                            ("P", "Playing"),
                            ("D", "Dropped"),
                            ("OH", "On hold"),
                        ],
                        max_length=3,
                        verbose_name="status",
                    ),
                ),
                (
                    "creation_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="last modified"),
                ),
            ],
            options={
                "verbose_name": "game list",
                "verbose_name_plural": "game lists",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
            ],
            options={
                "verbose_name": "genre",
                "verbose_name_plural": "genres",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Platform",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
            ],
            options={
                "verbose_name": "platform",
                "verbose_name_plural": "platforms",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
            ],
            options={
                "verbose_name": "publisher",
                "verbose_name_plural": "publishers",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GameReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "score",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name="score",
                    ),
                ),
                (
                    "creation_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
                ),
                ("review", models.TextField(blank=True, verbose_name="description")),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reviews",
                        to="games.game",
                    ),
                ),
            ],
            options={
                "verbose_name": "game review",
                "verbose_name_plural": "games reviews",
                "abstract": False,
            },
        ),
    ]
