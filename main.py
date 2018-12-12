from drafter.draft import PdfDraft
from report import Page1, Page2
from report.common.utils import clean_xls_headers, process_sht
from report.common.boiler import import_titles

import pandas as pd

#TODO: error handling module
error = []

class report(object):
    def __init__(self, gc, data_sht, meta_sht, faq_sht):
        self.data_sht = data_sht
        self.meta_sht = meta_sht
        self.faq_sht = faq_sht

        self.gc = gc

    def _get_faq(self, faq_num):
        """get FAQ values. if no FAQ specified or invalid, go to default"""
        #TODO: collect error here for when invalid or not in list
        if faq_num not in self.faq_sht.index:
            faq_num = self.meta_sht.loc['Default FAQ']['value']

        return {'q': self.faq_sht.loc[faq_num]['question'], 'a': self.faq_sht.loc[faq_num]['answer']}

    def create_data(self):
        cp = self.data_sht.loc[self.gc]

        self.data =  {
            #Date
            'rep_data': {
                'month': self.meta_sht.loc['Report Month']['value'],
                'year' : self.meta_sht.loc['Report Year']['value'],
                'dist_nm': cp['district_name'],
                'palika_nm': cp['palika_name'],
            },

            # Facts and figures
            #title
            'facts_and_figures': {
                'd1' : cp['damage_grade_1-2_cnt'],
                'd3' : cp['damage_grade_3-5_cnt']
            },

            # Major Housing Typologies
            # very hacky work around with a lookup table as an iterator
            'housing_typologies':
                    [{
                        'nm_look' : i[1],
                        'muni_pct' : cp['%s_municipal_pct' % i[0]],
                        'dist_pct' : cp['%s_district_pct' % i[0]]}
                        for i in
                            [('stone_and_cement' , 'typologies_stone_and_cement_mortar_masonry_row_title'),
                            ('stone_and_mud' , 'typologies_stone_and_mud_mortar_masonry_row_title'),
                            ('brick_and_cement' , 'typologies_brick_and_cement_mortar_masonry_row_title'),
                            ('brick_and_mud' , 'typologies_brick_and_mud_mortar_masonry_row_title'),
                            ('rcc_frame' , 'typologies_reinforced_cement_concrete_(rcc)_frame_row_title'),
                            ('hybrid' , 'typologies_hybrid_structure_row_title'),
                            ('timber_frame' , 'typologies_timber_frame_structure_row_title'),
                            ('hollow_concrete' , 'typologies_hollow_concrete_block_masonry_row_title'),
                            ('dry_stone' , 'typologies_dry_stone_masonry_row_title'),
                            ('adobe' , 'typologies_adobe_structures_row_title'),
                            ('bamboo' , 'typologies_bamboo_row_title'),
                            ('sceb' , 'typologies_compressed_stabilized_earth_block_(sceb)_masonry_row_title'),
                            ('light_steel' , 'typologies_light_steel_frame_structures_row_title')]
                    ],

            # Housing Reconstruction & Retrofit Updates
            'reconstruction_retrofit_updates': {
                'reconstruction_status': [
                    #title
                    {'label': 'recon_&_retrofit_total_eligible_hhs_(both)', 'value1' : cp['total_eligible_hhs_(reconstruction)'], 'value2': 0},

                    {'label': 'recon_&_retrofit_pa_agreement_(both)', 'value1' : cp['pa_agreement_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['pa_agreement_cnt_(reconstruction)']},

                    {'label': 'recon_&_retrofit_ist_tranche_received_(both)', 'value1' : cp['1st_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['1st_tranche_cnt_(reconstruction)']},

                    {'label': 'recon_&_retrofit_iind_tranche_received_(both)', 'value1' : cp['2nd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['2nd_tranche_cnt_(reconstruction)']},

                    {'label': 'recon_&_retrofit_iiird_tranche_received', 'value1' : cp['3rd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['3rd_tranche_cnt_(reconstruction)']}
                ],

                'houses': {
                    'under_construction': cp['houses_under_construction_cnt'],
                    'completed': cp['houses_completed_cnt'],
                },

                'retrofitting_status': [
                    {'label': 'recon_&_retrofit_total_eligible_hhs_(both)', 'value1': cp['total_eligible_hhs_(retrofit)'], 'value2': 0},

                    {'label': 'recon_&_retrofit_pa_agreement_(both)', 'value1': cp['pa_agreement_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['pa_agreement_cnt_(retrofit)']},

                    {'label': 'recon_&_retrofit_ist_tranche_received_(both)', 'value1': cp['1st_tranche_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['1st_tranche_cnt_(retrofit)']},

                    {'label': 'recon_&_retrofit_iind_tranche_received_(both)', 'value1': cp['2nd_tranche_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['2nd_tranche_cnt_(retrofit)']},
                ],

                'grievances': {
                    'registered': cp['grievances_registered_cnt'],
                    'addressed': cp['grievances_addressed_cnt'],
                },

                'non_compliances': {
                    'registered': cp['non_comp_registered_cnt'],
                    'addressed': cp['non_comp_addressed_cnt'],
                },
            },

            # POs Presence
            'pos_presence': {
                'active': (cp['active_pos_list']),
                'passive': (cp['phased_out_pos_list']),
            },

            # Other Sectors
            'other_sectors': {
                'schools': {
                    'damaged': cp['schools_damaged_cnt'],
                    'under_construction': cp['school_completed_cnt'],
                    'const_comp': cp['school_completed_cnt'],
                },
                'health_posts': {
                    'damaged': cp['health_posts_damaged_cnt'],
                    'under_construction': cp['health_posts_under_const_cnt'],
                    'const_comp': cp['health_posts_completed_cnt'],
                },
            },

            # Status of construction materials
            # title in cm_table
            'construction_materials': {
                m : {'req_quantity': cp['%s_required_quantity' % m] , 'ava': cp['%s_availability' % m],
                        'cost': cp['%s_cost' % m]}
                for m in ['stone', 'aggregate', 'sand', 'timber', 'cement_ppc', 'cement_opc', 'rebar', 'tin', 'bricks']},

            # Workers and wages
            'work_wage': {v : cp[v] for v in ['avg_wage_1', 'avg_wage_2']},

            # Key contacts
            'key_contacts': [
                {
                    'office': cp['contact_%i_title' % c],
                    'name': cp['contact_%i_name' % c],
                    'title': cp['contact_%i_role' % c],
                    'contact': str(cp['contact_%i_contact' % c])
                } for c in range(1,6)],

            # HHs with Land Issues
            'hhs': {
                'landless': cp['landless_cnt'],
                'right_of_way': cp['right_of_way_cnt'],
                'no_land_certificates': cp['no_land_cert_cnt'],
                'smallplots': cp['small_plots_cnt'],
                'guthi_land': cp['guthi_land_cnt'],
            },

            # Status of technical staff
            #title
            'technical_staff': [
                {'label': 'Engineers', 'available': cp['engineers_available_cnt'],
                        'additional': cp['engineers_reqd_cnt']},
                {'label': 'Sub-Engineers', 'available': cp['sub-engineers_available_cnt'],
                        'additional': cp['sub-engineers_reqd_cnt']},
                {'label': 'Asst. Sub-Engineers', 'available': cp['asst_sub-engineers_available_cnt'],
                        'additional': cp['asst_sub-engineers_reqd_cnt']}
            ],

            # Status of Masons
            'technical_staff_masons' :
                {'label': 'Masons',
                        'available': [cp['masons_7_day_available_cnt'], cp['masons_50_day_available_cnt']],
                        'additional': [cp['masons_7_day_reqd_cnt'], cp['masons_50_day_reqd_cnt']]}
            ,

            # Trainings
            'trainings': {
                'short': {
                    'reached': cp['short_training_reached_cnt'],
                    'remaining': cp['short_training_remaining_cnt'],
                },
                'vocational': {
                    'reached': cp['voc_training_reached_cnt'],
                    'remaining': cp['voc_training_remaining_cnt'],
                },
            },

            # MAP
            'map': {'map_uri' : './resources/maps/%s.png' % self.gc, 'legend_uri' : './resources/images/map_legend.png'},

            # FAQ
            'faq': [
                {
                    'q': self._get_faq(cp['faq_number'])['q'],
                    'a': self._get_faq(cp['faq_number'])['a']
                },
            ],

            #Further info
            'further_info': [
                {
                    'name': 'Reshma Shrestha',
                    'title': 'Dist. Coordinator',
                    'phone': '9841264190',
                },
                {
                    'name': 'Ishwor Neupane',
                    'title': 'Dist. IM Officer',
                    'phone': '9841264190',
                },
            ],
        }

def generate():
    XLS_URI = './resources/data/profile_data_structure_template.xlsx'

    #TODO: test sheets OK?
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

    #TODO: process the rest 2
    titles = process_sht(titles)
    titles.rename(lambda x: x.strip('#'), axis='rows', inplace = True)
    titles = clean_xls_headers(titles, 1)
    import_titles(titles)

    data = clean_xls_headers(data, 2)
    meta = clean_xls_headers(meta, 1)
    faq = clean_xls_headers(faq, 1)


    for v in data.index.values[0:1]:
        print('running for %s' %v)
        cur_rep = report(gc = v, data_sht = data, meta_sht = meta, faq_sht = faq)
        cur_rep.create_data()

        PdfDraft('./output/%s.pdf' %v)\
            .draw(Page1(cur_rep.data))\
            .draw(Page2(cur_rep.data))

if __name__ == '__main__':
    generate()