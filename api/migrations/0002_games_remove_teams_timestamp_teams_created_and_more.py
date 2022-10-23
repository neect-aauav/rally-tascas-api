# Generated by Django 4.1.2 on 2022-10-19 16:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default=None)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='teams',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='teams',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teams',
            name='has_egg',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Prizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('ammount', models.IntegerField()),
                ('winner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.teams')),
            ],
        ),
        migrations.AddField(
            model_name='bars',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.games'),
        ),
    ]