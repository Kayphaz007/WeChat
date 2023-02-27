# Generated by Django 4.1 on 2022-09-15 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("IndexApp", "0003_alter_message_room"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="message",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]