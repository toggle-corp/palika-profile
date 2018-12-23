import os

from drafter.draft import PdfDraft
from report import Page1, Page2
from report.common.utils import clean_xls_headers, process_sht, gen_maps
from report.common.Report import Report
from report.common.boiler import import_titles, set_lang

import pandas as pd

#TODO: error handling module
error = []

skip = ['51004',
'51005',
'51006',
'51002',
'51003',
'45001',
'45002',
'45006',
'45007',
'45003',
'45004',
'45005',
'45008',
'45009',
'45010',
'10005',
'10006',
'10007',
'10008',
'10001',
'10002',
'10003',
'10004',
'10009',
'35001',
'35005',
'35006',
'35002',
'35003',
'35004',
'35007',
'30001',
'30002',
'30003',
'30004',
'30005',
'30007',
'30008',
'30009',
'30010',
'7001',
'7002',
'30006',
'30011',
'30012',
'30013',
'7003',
'22004',
'22005',
'22006',
'7004',
'7005',
'7006',
'7007',
'22001',
'22002',
'22003',
'22007',
'22008',
'22009',
'51001',
'36005',
'36006',
'36002',
'36003',
'36004',
'36007',
'36008',
'36009',
'46003',
'46004',
'46005',
'46006',
'36010',
'36011',
'46001',
'46002',
'46007',
'46008',
'46012',
'40001',
'46009',
'46010',
'46011',
'40002',
'40003',
'40004',
'40005',
'26001',
'26002',
'26004',
'27001',
'27002',
'27003',
'27007',
'27008',
'26003',
'27004',
'27005',
'27006',
'27009',
'27010',
'27011',
'25001',
'36001',
'25004',
'25002',
'25003',
'25005',
'25006',
'24001',
'24002',
'24005',
'24006',
'24003',
'24004',
'24007',
'24008',
'24013',
'13001',
'13002',
'13003',
'24009',
'24010',
'24011',
'24012',
'13004',
'13005',
'13009',
'13010',
'13006',
'13007',
'13008',
'37001',
'37002',
'37003',
'37004',
'37005',
'37006',
'37008',
'31001',
'31002',
'31003',
'31007',
'31008',
'37007',
'31004',
'31005',
'31006',
'31009',
'43006',
'48001',
'48002',
'48003',
'31010',
'43001',
'43002',
'43003',
'43004',
'43005',
'48004',
'48009',
'48010',
'48011',
'48005',
'48006',
'48007',
'48012',
'48008']


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
        if str(v) not in skip:
            print('Creating profile for %s' %v)
            cur_rep = Report(gc = v, data_sht = data, meta_sht = meta, faq_sht = faq, map_img_type = map_img_type)
            cur_rep.create_data()

            os.makedirs('./output/', exist_ok=True)
            PdfDraft('./output/%s_%s.pdf' %(v, lang_in))\
                .draw(Page1(cur_rep.data, lang_in))\
                .draw(Page2(cur_rep.data, lang_in))



if __name__ == '__main__':
    # generate(lang_in='en', test_len=1, make_maps=False, map_img_type='svg')
    generate(lang_in='en', test_len=None, make_maps=False, map_img_type='svg')

