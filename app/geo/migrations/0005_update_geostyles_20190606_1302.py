import os
from django.db import migrations
from django.core.files import File
from django.conf import settings
from django.core.management import call_command


def update_geostyles(apps, schema_editor):
    GeoStyle = apps.get_model('geo', 'GeoStyle')
    GeoStyleFile = apps.get_model('geo', 'GeoStyleFile')

    GeoStyle.objects.all().delete()

    call_command('loaddata', 'initial_geo.json', app_label='geo')

    for geostylefile in GeoStyleFile.objects.all():
        filename = geostylefile.file.name
        filepath = os.path.join(settings.BASE_DIR, filename)
        with open(filepath, 'rb') as fp:
            geostylefile.file = File(fp, filename.split('/')[-1])
            geostylefile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0004_auto_20190606_1301'),
    ]

    operations = [
        migrations.RunPython(update_geostyles),
    ]
