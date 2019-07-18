# Generated by Django 2.1.7 on 2019-03-18 06:22

from django.db import migrations
from django.core.management import call_command


def load_initial_palika_codes(apps, schema_editor):
    call_command('loaddata', 'initial_palika.json', app_label='geo')


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        # NOTE: Don't Need this now
        # migrations.RunPython(load_initial_palika_codes),
    ]
