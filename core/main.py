import os

from drafter.draft import PdfDraft
from report import Page1, Page2
from report.common.utils import gen_maps
from report.common.Report import Report
from report.common.boiler import set_lang
from report.common.Sheet import Sheet
from report.common import XLS_URI, SHT_RESERVE_CHAR

import pandas as pd

OUTPUT_PATH = './output/'
PDF_TITLE = '%s_%s.pdf'
PDF_WRITE_PATH = OUTPUT_PATH + PDF_TITLE


def generate(
        skip=[], lang_in='en', test_len=None, make_maps=False, make_scnd=True,
        map_img_type='svg', overwrite=False,
):

    set_lang(lang_in)

    # read in sheets
    # TODO: test sheets are OK?
    # TODO: more pythonic way of passing args
    data = Sheet(
        pd.read_excel(
            XLS_URI, sheet_name='Profile Data', index_col=0, header=0,
        ),
        skip=skip,
        test_len=test_len,
        overwrite=overwrite,
        OUTPUT_PATH=OUTPUT_PATH,
        lang_in=lang_in,

        num_rows_strip=3,
        remove_reserve_dims='columns',
        reserve_val=SHT_RESERVE_CHAR,
        process_specific='data'
    )
    # for now, all data is processed regardless of it is filtered or not
    data.process()

    print('Errors for data:')
    # print(data.errors)

    meta = Sheet(
        pd.read_excel(XLS_URI, sheet_name='Meta', index_col=0, header=0),
        num_rows_strip=1,
        remove_reserve_dims='columns',
        reserve_val=SHT_RESERVE_CHAR
    )
    meta.process()

    faq = Sheet(
        pd.read_excel(XLS_URI, sheet_name='FAQs', index_col=0, header=0),
        num_rows_strip=1,
        remove_reserve_dims='columns',
        reserve_val=SHT_RESERVE_CHAR
    )
    faq.process()

    titles = Sheet(
        pd.read_excel(XLS_URI, sheet_name='titles', index_col=0, header=0),
        num_rows_strip=1,
        remove_reserve_dims=['rows', 'columns'],
        reserve_val=SHT_RESERVE_CHAR,
        process_specific='titles'
    )
    titles.process()

    # clean sheets
    # # TODO: process the rest 2
    # titles = process_sht(titles)
    # titles.rename(lambda x: x.strip('#'), axis='rows', inplace = True)
    # import_titles(titles)
    #
    # data = clean_xls_headers(data, 2)
    # meta = clean_xls_headers(meta, 1)
    # faq = clean_xls_headers(faq, 1)

    palika_codes = data.sht.index[:test_len] if test_len else data.sht.index

    if make_maps:
        gen_maps(list(palika_codes), map_img_type)

    # process
    print('Creating for: ', data.sht.index.values)

    for v in palika_codes:
        print('Creating profile for %s' % v)
        cur_rep = Report(gc=v, data_sht=data.sht, meta_sht=meta.sht,
                         faq_sht=faq.sht, map_img_type=map_img_type)
        cur_rep.create_data()

        os.makedirs(OUTPUT_PATH, exist_ok=True)
        pdf_draft = PdfDraft(PDF_WRITE_PATH % (v, lang_in)) \
            .draw(Page1(cur_rep.data, lang_in))
        if make_scnd:
            pdf_draft.draw(Page2(cur_rep.data, lang_in))
        pdf_draft.surface.__exit__()


if __name__ == '__main__':
    # generate(
    #     # test_len=5,
    #     lang_in='en',
    #     # make_maps=True,
    #     make_scnd=True,
    #     map_img_type='svg',
    #     overwrite=True,
    # )

    generate(
        test_len=1,
        lang_in='en',
        make_maps=False,
        make_scnd=True,
        map_img_type='svg',
        overwrite=True,
    )
