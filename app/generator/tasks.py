import logging
import traceback

from django.db import transaction

from config.celery import app
from .models import (
    Generator,
)
from .utils import generator as pdf_generator, validator

logger = logging.getLogger(__name__)


@app.task(bind=True)
def generate_pdf(self, id):
    try:
        with transaction.atomic():
            # Celery state
            self.update_state(state='PROGRESS')
            self.job_meta = {}
            generator = Generator.objects.get(pk=id)
            generator.exports.all().delete()
            pdf_generator.generate(
                self, generator,
                lang_in='en',
                test_len=10,
                make_maps=False,
                make_scnd=True,
                map_img_type='svg',
                overwrite=True,
            )
            generator.data = self.job_meta
            generator.status = Generator.SUCCESS
    except Exception:
        generator.status = Generator.FAILURE
        generator.data = {
            **self.job_meta,
            'errors': traceback.format_exc(),
        }
        logger.error('Failed to generator pdf for ({})'.format(id), exc_info=1)
    generator.save()
    return generator.status


@app.task(bind=True)
def test_doc(self, id):
    try:
        with transaction.atomic():
            # Celery state
            self.update_state(state='PROGRESS')
            self.job_meta = {}
            generator = Generator.objects.get(pk=id)
            errors = validator.validate(self, generator)
            generator.errors = errors
            generator.save()
    except Exception:
        logger.error(
            'Failed to test generator for ({})'.format(id),
            exc_info=1,
        )
        return Generator.FAILURE
    return Generator.SUCCESS
