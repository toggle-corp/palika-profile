import shutil
import os
from django.utils.crypto import get_random_string


class CoreConfig():
    OUTPUT_PATH_FORMAT = '/tmp/core/{}/'

    def __init__(self):
        self.output_path = self.OUTPUT_PATH_FORMAT.format(
            get_random_string(length=7),
        )

    def get_output_path(self):
        return self.output_path

    def get_pdf_write_path(self, pdf_title_format, *args, **kwargs):
        pdf_path_format = os.path.join(self.output_path, pdf_title_format)
        return pdf_path_format.format(*args, **kwargs)

    def clean_ouput_path(self):
        # TODO: Remove from S3 if used
        directory = self.get_output_path()
        if os.path.isdir(directory):
            shutil.rmtree(directory)
