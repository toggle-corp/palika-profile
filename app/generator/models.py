import os

from django.db import models
from django.contrib.postgres.fields import JSONField


class TaskModel(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUSES = (
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure'),
    )

    status = models.CharField(max_length=30, choices=STATUSES, default=PENDING)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Generator(TaskModel):
    file = models.FileField(upload_to='documents/', max_length=255)
    errors = JSONField(default=dict, null=True, blank=True)
    data = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_file = self.file

    def __str__(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]


class Export(models.Model):
    file = models.FileField(upload_to='exports/', max_length=255)
    generator = models.ForeignKey(
        Generator,
        on_delete=models.CASCADE,
        related_name='exports',
    )

    def __str__(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]
