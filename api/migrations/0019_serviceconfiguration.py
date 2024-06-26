# Generated by Django 4.2.11 on 2024-04-18 00:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_messagetemplate"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceConfiguration",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=200)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
