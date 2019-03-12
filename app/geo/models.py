from django.db import models


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

    def __str__(self):
        return self.get_geo_type_display()


class GeoStyle(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='style_files/', max_length=255)
    geoarea = models.ForeignKey(
        GeoArea, on_delete=models.CASCADE, blank=True, null=True,
    )

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
