# Generated by Django 5.0.6 on 2024-07-27 21:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_bot', '0013_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='matches',
            field=models.ManyToManyField(blank=True, related_name='my_matches', to=settings.AUTH_USER_MODEL),
        ),
    ]
