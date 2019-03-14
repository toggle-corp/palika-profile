import os
from django.db import models


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

    def get_file_path(self):
        file_uri = os.path.join(GEOJSON_FILE_DIR, self.file.name)
        if os.path.isfile(file_uri):
            return file_uri
        with open(file_uri, 'wb') as fp:
            fp.write(self.file.read())
        return file_uri

    def __str__(self):
        return self.get_geo_type_display()


class GeoStyle(models.Model):
    DISTRICT_STYLE = 'district_style'
    PALIKA_HIDE_STYLE = 'palika_hide_style'
    ATLAS_STYLE = 'atlas_style'
    WARD_STYLE = 'ward_style'
    PALIKA_EN_STYLE = 'palika_en_style'
    PALIKA_NP_STYLE = 'palika_np_style'

    STYLE_TYPES = (
        (DISTRICT_STYLE, 'District Style'),
        (PALIKA_HIDE_STYLE, 'Palika Hide Style'),
        (ATLAS_STYLE, 'Atlas Style'),
        (WARD_STYLE, 'Ward Style'),
        (PALIKA_EN_STYLE, 'Palika en Style'),
        (PALIKA_NP_STYLE, 'Palika np Style'),
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='style_files/', max_length=255)
    style_type = models.CharField(max_length=30, choices=STYLE_TYPES, unique=True)

    def get_file_path(self):
        file_uri = os.path.join(GEO_STYE_FILE_DIR, self.file.name)
        if os.path.isfile(file_uri):
            return file_uri
        with open(file_uri, 'wb') as fp:
            fp.write(self.file.read())
        return file_uri

    def __str__(self):
        return self.title


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


def get_map_params_for_generation():
    ward_uri = GeoArea.get_file_path(geo_type=GeoArea.WARD)
    palika_uri = GeoArea.get_file_path(geo_type=GeoArea.PALIKA)
    district_uri = GeoArea.get_file_path(geo_type=GeoArea.DISTRICT)

    district_style_uri = GeoStyle.get_file_path(geo_type=GeoStyle.DISTRICT_STYLE)
    palika_hide_style_uri = GeoStyle.get_file_path(geo_type=GeoStyle.PALIKA_HIDE_STYLE)
    atlas_style_uri = GeoStyle.get_file_path(geo_type=GeoStyle.ATLAS_STYLE)
    ward_style_uri = GeoStyle.get_file_path(geo_type=GeoStyle.WARD_STYLE)
    pka_style_lang_uri = GeoStyle.get_file_path(geo_type=GeoStyle.PALIKA_EN_STYLE)

    return {
        # Shapes
        'wards_uri': ward_uri,
        'palika_uri': palika_uri,
        'dists_uri': district_uri,
        # Styles
        'dists_style_uri': district_style_uri,
        'pka_hide_style_uri': palika_hide_style_uri,
        'atlas_style_uri': atlas_style_uri,
        'ward_style_uri': ward_style_uri,
        'pka_style_lang_uri': pka_style_lang_uri,
    }
