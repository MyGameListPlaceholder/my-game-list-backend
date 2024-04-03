# Generated by Django 4.2.4 on 2024-04-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("X", "Prefer not to say")],
                default="X",
                max_length=1,
                verbose_name="gender",
            ),
        ),
    ]
