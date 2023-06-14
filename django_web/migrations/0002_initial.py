# Generated by Django 4.1.7 on 2023-05-05 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("django_web", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Douban",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mv_rank", models.IntegerField()),
                ("mv_name", models.CharField(max_length=32)),
                ("mv_star", models.CharField(max_length=32)),
                ("mv_quote", models.CharField(max_length=321)),
                ("addtime", models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={"db_table": "movie",},
        ),
        migrations.CreateModel(
            name="Novel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nv_type", models.CharField(max_length=32)),
                ("nv_name", models.CharField(max_length=32)),
                ("nv_author", models.CharField(max_length=32)),
                ("nv_new_chapter", models.CharField(max_length=32)),
                ("nv_recommend", models.CharField(max_length=32)),
                ("addtime", models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={"db_table": "novel",},
        ),
        migrations.CreateModel(
            name="Weather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.CharField(max_length=32)),
                ("max_temperature", models.CharField(max_length=32)),
                ("min_temperature", models.CharField(max_length=32)),
                ("wea_condition", models.CharField(max_length=32)),
                ("wea_quality", models.CharField(max_length=32)),
                ("wind", models.CharField(max_length=32)),
                ("addtime", models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={"db_table": "weather",},
        ),
    ]
