# Generated by Django 4.1.2 on 2022-10-25 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_teams_email_teams_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='points',
        ),
    ]