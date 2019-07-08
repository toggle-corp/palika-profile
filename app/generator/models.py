import os

from django.db import models
from django.contrib.postgres.fields import JSONField

from geo.models import GeoStyleFile


class TaskModel(models.Model):
    NOT_PROCESSED = 'not_processed'
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUSES = (
        (NOT_PROCESSED, 'Not Processed'),
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure'),
    )

    status = models.CharField(
        max_length=30, choices=STATUSES, default=NOT_PROCESSED,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Generator(TaskModel):
    file = models.FileField(upload_to='documents/', max_length=255)
    errors = JSONField(default=dict, null=True, blank=True)
    data = JSONField(default=dict, null=True, blank=True)
    geo_meta = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_file = self.file

    def __str__(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]


class Export(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='exports/', max_length=255)
    palika_code = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(
        max_length=30, choices=GeoStyleFile.LANGUAGE_CHOICES, default=GeoStyleFile.ENGLISH,
    )
    generator = models.ForeignKey(
        Generator,
        on_delete=models.CASCADE,
        related_name='exports',
    )

    def __str__(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]
