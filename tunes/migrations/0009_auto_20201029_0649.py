# Generated by Django 2.0.6 on 2020-10-29 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0008_song_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songcategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]