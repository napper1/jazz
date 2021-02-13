# Generated by Django 2.0.6 on 2021-01-07 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0009_auto_20201029_0649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='songcategory',
            options={'verbose_name': 'Song Category', 'verbose_name_plural': 'Song Categories'},
        ),
        migrations.AddField(
            model_name='song',
            name='spotify',
            field=models.BooleanField(default=False, verbose_name='Spotify Track'),
        ),
    ]
