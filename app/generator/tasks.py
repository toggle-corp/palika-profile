import shutil
import logging
import traceback

from django.db import transaction
from django.core.files import File

from config.celery import app

from .models import (
    Generator,
    Export,
)
from common.utils import CoreConfig
from .utils import generator as pdf_generator, validator

logger = logging.getLogger(__name__)


@transaction.atomic
def _generate_pdf(self, cc, generator):
    # Celery state
    self.update_state(state='PROGRESS')
    self.job_meta = {}

    # Delete previous exports
    generator.exports.all().delete()

    # Generate new exports
    pdf_files, errors = pdf_generator.generate(
        self,
        cc,
        generator.file,
        lang_in='en',
        test_len=5,
        make_maps=False,
        make_scnd=True,
        map_img_type='svg',
        overwrite=True,
    )

    # Save files to Generator
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as fp:
            Export.objects.create(
                generator=generator,
                file=File(fp, pdf_file.split('/')[-1]),
            )

    generator.errors = errors
    generator.data = self.job_meta
    generator.status = Generator.SUCCESS


@app.task(bind=True)
def generate_pdf(self, id):
    cc = CoreConfig()
    generator = Generator.objects.get(pk=id)
    try:
        _generate_pdf(self, cc, generator)
    except Exception:
        generator.status = Generator.FAILURE
        generator.data = {
            **self.job_meta,
            'errors': traceback.format_exc(),
        }
        logger.error('Failed to generator pdf for ({})'.format(id), exc_info=1)
    # Clean generator files
    shutil.rmtree(cc.get_output_path())
    generator.save()
    return generator.status


@app.task(bind=True)
def test_doc(self, id):
    cc = CoreConfig()
    try:
        with transaction.atomic():
            # Celery state
            self.update_state(state='PROGRESS')
            self.job_meta = {}
            generator = Generator.objects.get(pk=id)
            errors = validator.validate(self, cc, generator)
            generator.errors = errors
            generator.save()
    except Exception:
        logger.error(
            'Failed to test generator for ({})'.format(id),
            exc_info=1,
        )
        return Generator.FAILURE
    # Clean generator files
    shutil.rmtree(cc.get_output_path())
    return Generator.SUCCESS
