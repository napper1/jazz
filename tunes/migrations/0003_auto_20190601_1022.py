# Generated by Django 2.0.6 on 2019-06-01 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0002_song_downloaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('video_id', models.CharField(blank=True, max_length=11, primary_key=True, serialize=False)),
                ('video_title', models.TextField(blank=True, db_index=True, null=True)),
                ('moods', models.CharField(choices=[('HAPPY', 'Happy'), ('IN-LOVE', 'In-Love'), ('SAD', 'Sad'), ('CONFIDENT-SASSY', 'Confident-sassy'), ('CHILL', 'Chill'), ('ANGRY', 'Angry')], default='HAPPY', max_length=20)),
                ('labeled', models.NullBooleanField()),
                ('video_description', models.TextField(blank=True, null=True)),
                ('predicted_moods', models.CharField(blank=True, max_length=17, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['-id']},
        ),
    ]