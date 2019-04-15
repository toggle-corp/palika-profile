import os
import logging

import pandas as pd

from drafter.draft import PdfDraft
from core.report import Page1, Page2
from core.report.common.utils import gen_maps
from core.report.common.Report import Report
from core.report.common.boiler import set_lang
from core.report.common.Sheet import Sheet
from core.report.common import SHT_RESERVE_CHAR

logger = logging.getLogger(__name__)


def generate(
        self,
        cc,
        file,
        selected_palika_codes,
        map_params,
        skip=[],
        lang_in='en',
        test_len=None,
        make_maps=False,
        make_scnd=True,
        map_img_type='svg',
        overwrite=False,
):
    job_progress = {
        'itemList': ['titles', 'faq', 'pdf'],
        'items': {},
    }
    job_palika_progress = {}

    def update_meta(state):
        if self:
            self.job_meta.update(state)
            self.update_state(meta=self.job_meta)

    def update_progress(state):
        job_progress['items'].update(state)
        update_meta({'progress': job_progress})

    def update_palika_progress(state):
        job_palika_progress.update(state)
        update_progress(job_palika_progress)

    set_lang(lang_in)

    os.makedirs(cc.get_output_path(), exist_ok=True)
    data = Sheet(
        pd.read_excel(
            file, sheet_name='Profile Data', index_col=0, header=0,
        ),
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

    faq = Sheet(
        pd.read_excel(
            file, sheet_name='FAQs', index_col=0, header=0,
        ),
        num_rows_strip=1,
        remove_reserve_dims='columns',
        reserve_val=SHT_RESERVE_CHAR
    )
    faq.process()
    update_progress({'faq': 100})

    titles = Sheet(
        pd.read_excel(
            file, sheet_name='titles', index_col=0, header=0,
        ),
        num_rows_strip=1,
        remove_reserve_dims=['rows', 'columns'],
        reserve_val=SHT_RESERVE_CHAR,
        process_specific='titles'
    )
    titles.process()
    update_progress({'titles': 100})

    palika_codes = selected_palika_codes or (
        data.sht.index[:test_len] if test_len else data.sht.index
    )

    if make_maps:
        gen_maps(list(palika_codes), map_img_type, **map_params)
        update_progress({'maps': 100})

    total_palika = len(palika_codes)
    completed = 0
    pdf_files = []
    update_palika_progress({
        'pdf': {
            'total': total_palika,
            'complete': completed,
        },
    })
    for v in palika_codes:
        print('Creating profile for {}'.format(v))
        cur_rep = Report(gc=v, data_sht=data.sht, faq_sht=faq.sht, map_img_type=map_img_type)
        cur_rep.create_data()

        pdf_file_path = cc.get_pdf_write_path('{}_{}.pdf', v, lang_in)
        pdf_draft = PdfDraft(pdf_file_path).draw(Page1(cur_rep.data, lang_in))
        if make_scnd:
            pdf_draft.draw(Page2(cur_rep.data, lang_in))

        pdf_draft.surface.__exit__()
        pdf_files.append([v, pdf_file_path])
        completed += 1
        update_palika_progress({
            'pdf': {
                'total': total_palika,
                'complete': completed,
            },
        })

    return pdf_files, data.errors
