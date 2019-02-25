# Generated by Django 2.1.3 on 2019-02-21 11:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='generator',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 2, 21, 11, 27, 22, 147405, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generator',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]