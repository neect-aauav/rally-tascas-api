# Generated by Django 4.1.2 on 2022-10-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_bars_game_alter_prizes_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bars',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='games',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]