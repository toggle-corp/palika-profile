import logging
import traceback

from django.db import transaction
from django.core.files import File

from config.celery import app

from geo.models import get_map_params_for_generation
from .models import (
    Generator,
    Export,
)
from common.utils import CoreConfig
from .utils import generator as pdf_generator, validator

logger = logging.getLogger(__name__)


@transaction.atomic
def _generate_pdf(self, cc, generator, selected_palika_codes, language):
    # Celery state
    self.update_state(state='PROGRESS')

    # Delete previous exports
    generator.exports.all().delete()

    map_params = get_map_params_for_generation(language)

    # Generate new exports
    pdf_files, errors = pdf_generator.generate(
        self,
        cc,
        generator.file,
        selected_palika_codes,
        map_params,
        lang_in=language,
        make_maps=True,
        make_scnd=True,
        map_img_type='svg',
        overwrite=True,
    )

    # Save files to Generator
    for palika_code, pdf_file in pdf_files:
        with open(pdf_file, 'rb') as fp:
            Export.objects.create(
                title=pdf_file.split('/')[-1],
                generator=generator,
                file=File(fp, pdf_file.split('/')[-1]),
                palika_code=palika_code,
            )

    generator.errors = errors
    generator.data = self.job_meta
    generator.status = Generator.SUCCESS


@app.task(bind=True)
def generate_pdf(self, id, selected_palika_codes=None, language='en'):
    cc = CoreConfig()
    generator = Generator.objects.get(pk=id)
    self.job_meta = {}
    try:
        _generate_pdf(self, cc, generator, selected_palika_codes, language)
    except Exception:
        generator.status = Generator.FAILURE
        generator.data = {
            **self.job_meta,
            'errors': traceback.format_exc(),
        }
        logger.error('Failed to generator pdf for ({})'.format(id), exc_info=1)
    # Clean generator files
    cc.clean_ouput_path()
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
            errors, palika_codes = validator.validate(self, cc, generator.file)
            generator.errors = errors
            generator.geo_meta = {
                'palika_codes': list(set(palika_codes)),
            }
            generator.save()
    except Exception:
        logger.error(
            'Failed to test generator for ({})'.format(id),
            exc_info=1,
        )
        return Generator.FAILURE
    # Clean generator files
    cc.clean_ouput_path()
    return Generator.SUCCESS
