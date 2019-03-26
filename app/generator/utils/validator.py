import os

import pandas as pd

from core.report.common.Sheet import Sheet
from core.report.common import SHT_RESERVE_CHAR


def validate(
        self, cc, file, skip=[], lang_in='en', test_len=None,
        overwrite=False,
):
    job_progress = {
        'itemList': ['testing'],
        'items': {},
    }

    def update_meta(data):
        self.job_meta.update(data)
        self.update_state(meta=self.job_meta)

    def update_progress(data):
        job_progress['items'].update(data)
        update_meta({'progress': job_progress})

    os.makedirs(cc.get_output_path(), exist_ok=True)
    data = Sheet(
        pd.read_excel(file, sheet_name='Profile Data', index_col=0, header=0),
        skip=skip,
        test_len=test_len,
        overwrite=overwrite,
        OUTPUT_PATH=cc.get_output_path(),
        lang_in=lang_in,
        num_rows_strip=3,
        remove_reserve_dims='columns',
        reserve_val=SHT_RESERVE_CHAR,
        process_specific='data'
    )
    # for now, all data is processed regardless of it is filtered or not
    data.process()
    update_progress({'testing': 100})
    return data.errors, list(data.sht.index)
