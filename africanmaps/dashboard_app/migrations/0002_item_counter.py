# Generated by Django 5.1.2 on 2024-10-29 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='counter',
            field=models.IntegerField(default=1),
        ),
    ]