import logging
import os
from django.db import models

logger = logging.getLogger(__name__)

GEO_FILE_DIR = '/tmp/palika_geo/'
GEOJSON_FILE_DIR = os.path.join(GEO_FILE_DIR, 'geojsons')
GEO_STYE_FILE_DIR = os.path.join(GEO_FILE_DIR, 'styles')


class GeoArea(models.Model):
    WARD = 'ward'
    PALIKA = 'palika'
    DISTRICT = 'district'

    GEO_TYPES = (
        (WARD, 'Ward'),
        (PALIKA, 'Palika'),
        (DISTRICT, 'District'),
    )

    file = models.FileField(upload_to='shape_files/', max_length=255)
    geo_type = models.CharField(max_length=30, choices=GEO_TYPES, unique=True)

    @staticmethod
    def get_file_path(geo_type):
        geoarea = GeoArea.objects.filter(geo_type=geo_type).first()
        file_uri = os.path.join(GEOJSON_FILE_DIR, geoarea.file.name)
        if os.path.isfile(file_uri):
            return file_uri
        os.makedirs(os.path.dirname(file_uri), exist_ok=True)
        with open(file_uri, 'wb') as fp:
            fp.write(geoarea.file.read())
        return file_uri

    def __str__(self):
        return self.get_geo_type_display()


class GeoStyle(models.Model):
    DISTRICT_STYLE = 'district_style'
    PALIKA_HIDE_STYLE = 'palika_hide_style'
    ATLAS_STYLE = 'atlas_style'
    WARD_STYLE = 'ward_style'
    PALIKA_STYLE = 'palika_style'

    STYLE_TYPES = (
        (DISTRICT_STYLE, 'District Style'),
        (PALIKA_HIDE_STYLE, 'Palika Hide Style'),
        (ATLAS_STYLE, 'Atlas Style'),
        (WARD_STYLE, 'Ward Style'),
        (PALIKA_STYLE, 'Palika Style'),
    )

    title = models.CharField(max_length=255)
    style_type = models.CharField(max_length=30, choices=STYLE_TYPES, unique=True)

    @staticmethod
    def get_file_path(style_type, language, default_language):
        geostyle = GeoStyle.objects.filter(style_type=style_type).first()

        geostylefile = geostyle.geostylefile_set.filter(language=language).first()
        if geostylefile is None:  # NOTE: Use default style (EN)
            geostylefile = geostyle.geostylefile_set.filter(language=default_language).first()
            logger.warning(f'Style:{style_type} not set for LANG: {language}, Using Default Lang: {default_language}')
        if geostylefile is None:  # NOTE: This should never happen
            raise Exception(f'Default style not set for Style:{style_type}')

        file_uri = os.path.join(GEOJSON_FILE_DIR, geostylefile.file.name)
        if os.path.isfile(file_uri):
            return file_uri
        os.makedirs(os.path.dirname(file_uri), exist_ok=True)
        with open(file_uri, 'wb') as fp:
            fp.write(geostylefile.file.read())
        return file_uri

    def __str__(self):
        return self.title


class GeoStyleFile(models.Model):
    ENGLISH = 'en'
    NEPALI = 'np'

    LANGUAGE_CHOICES = (
        (ENGLISH, 'English (Default)'),
        (NEPALI, 'NEPALI'),
    )

    SUPPORTED_LANGUAGES = [lang for lang, _ in LANGUAGE_CHOICES]

    geo_style = models.ForeignKey(GeoStyle, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default=ENGLISH)
    file = models.FileField(upload_to='style_files/', max_length=255)

    class Meta:
        unique_together = ('language', 'geo_style')

    def __str__(self):
        return f'{self.geo_style.title} :: {self.get_language_display()}'


class Province(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Palika(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.title, self.code)


def get_map_params_for_generation(language='en'):
    areas_uri = {}
    styles_uri = {}

    for geoarea_key, geoarea_type in [
        ('wards_uri', GeoArea.WARD),
        ('palika_uri', GeoArea.PALIKA),
        ('dists_uri', GeoArea.DISTRICT),
    ]:
        areas_uri[geoarea_key] = GeoArea.get_file_path(geoarea_type)

    for style_key, style_type in [
        ('dists_style_uri', GeoStyle.DISTRICT_STYLE),
        ('pka_hide_style_uri', GeoStyle.PALIKA_HIDE_STYLE),
        ('atlas_style_uri', GeoStyle.ATLAS_STYLE),
        ('ward_style_uri', GeoStyle.WARD_STYLE),
        ('pka_style_lang_uri', GeoStyle.PALIKA_STYLE),
    ]:
        if language not in GeoStyleFile.SUPPORTED_LANGUAGES:
            raise Exception('Unknown Language {} supplied for map params'.format(language))
        styles_uri[style_key] = GeoStyle.get_file_path(style_type, language, GeoStyleFile.ENGLISH)

    return {
        # Shapes
        **areas_uri,
        # Styles
        **styles_uri,
    }
