# Generated by Django 4.1.2 on 2022-10-19 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_games_remove_teams_timestamp_teams_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='drinks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teams',
            name='puked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamsbars',
            name='drinks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamsbars',
            name='has_egg',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teamsbars',
            name='puked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teamsbars',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='MembersBars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('drinks', models.IntegerField(default=0)),
                ('barId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bars')),
                ('memberId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.members')),
            ],
        ),
    ]
