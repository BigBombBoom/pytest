# Generated by Django 4.2.1 on 2023-05-19 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_voterecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_only',
            field=models.BooleanField(default=False),
        ),
    ]
