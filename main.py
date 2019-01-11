import os

from drafter.draft import PdfDraft
from report import Page1, Page2
from report.common.utils import clean_xls_headers, process_sht, gen_maps
from report.common.Report import Report
from report.common.boiler import import_titles, set_lang

import pandas as pd

#TODO: error handling module
error = []


def generate(lang_in, test_len = None, make_maps = True, map_img_type ='svg'):
    set_lang(lang_in)
    XLS_URI = './resources/data/profile_data_structure_template.xlsx'

    #read in sheets

    #TODO: test sheets are OK?
    data = pd.read_excel(
            XLS_URI,
            sheet_name='Profile Data', index_col=0, header=0)

    meta = pd.read_excel(
            XLS_URI,
            sheet_name='Meta', index_col=0, header=0)

    faq = pd.read_excel(
            XLS_URI,
            sheet_name='FAQs', index_col=0, header=0)

    titles = pd.read_excel(
            XLS_URI,
            sheet_name='Titles', index_col=0, header=0)

    #clean sheets
    #TODO: process the rest 2
    titles = process_sht(titles)
    titles.rename(lambda x: x.strip('#'), axis='rows', inplace = True)
    titles = clean_xls_headers(titles, 1)
    import_titles(titles)

    data = clean_xls_headers(data, 2)
    meta = clean_xls_headers(meta, 1)
    faq = clean_xls_headers(faq, 1)

    #trim data if running  a test
    data = data[:test_len] if test_len else data

    if make_maps:
        gen_maps(list(data.index), map_img_type)

    #process
    for v in data.index.values:
        print('Creating profile for %s' %v)
        cur_rep = Report(gc = v, data_sht = data, meta_sht = meta, faq_sht = faq, map_img_type = map_img_type)
        cur_rep.create_data()

        os.makedirs('./output/', exist_ok=True)
        PdfDraft('./output/%s_%s.pdf' %(v, lang_in)) \
            .draw(Page1(cur_rep.data, lang_in))
            # .draw(Page2(cur_rep.data, lang_in))\


if __name__ == '__main__':
    # generate(lang_in='en', test_len=1, make_maps=False, map_img_type='svg')
    generate(lang_in='en', test_len=1, make_maps=False, map_img_type='svg')
    generate(lang_in='np', test_len=1, make_maps=False, map_img_type='svg')
