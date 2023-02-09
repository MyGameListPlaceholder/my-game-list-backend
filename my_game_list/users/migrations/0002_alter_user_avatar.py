# Generated by Django 4.1.3 on 2022-11-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.BinaryField(
                blank=True, editable=True, max_length=307200, null=True, verbose_name="avatar"
            ),
        ),
    ]
