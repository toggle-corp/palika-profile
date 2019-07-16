import os
from django.conf import settings
from django.core.management.base import BaseCommand

from generator.models import Export


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Deleting orphan exports...')
        media_directory = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)

        export_directory = os.path.join(media_directory, 'exports')
        exports = {
            export.file.path: True
            for export in Export.objects.all()
        }
        for file in os.listdir(export_directory):
            fullpath = os.path.join(export_directory, file)
            if not exports.get(fullpath):
                self.stdout.write(f'  >> Removing {fullpath}')
                os.remove(fullpath)
