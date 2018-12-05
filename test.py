from drafter.draft import PdfDraft
from report import Page1, Page2
from report.common.utils import fmt_pct

import pandas as pd

#TODO: error handling module
error = []

class report(object):
    def __init__(self, gc, sht):
        self.sht = sht
        self.gc = gc

    def create_data(self):
        cp = self.sht.loc[self.gc]

        self.data =  {
            # Facts and figures
            #title
            'facts_and_figures': {
                'data': [
                    {'label' : 'Damage Grade (1-2)', 'value' : cp['damage_grade_1-2_cnt']},
                    {'label' : 'Damage Grade (3-5)', 'value' : cp['damage_grade_3-5_cnt']},
                ],
            },

            # Major Housing Typologies
            'housing_typologies': {
                #title
                'headers': ['Typology', 'Municipal', 'District'],
                #title for types
                'data': [[cp['type_%i_name' % i],
                            fmt_pct(cp['type_%i_palika_pct' % i]),
                            fmt_pct(cp['type_%i_district_pct' % i])]
                         for i in range (1,7)]
                ,
            },

            # Housing Reconstruction & Retrofit Updates
            'reconstruction_retrofit_updates': {
                'reconstruction_status': [
                    #title
                    {'label': 'Total Eligible HHs', 'value1' : cp['total_eligible_hhs_(reconstruction)'], 'value2': 0},

                    {'label': 'PA Agreement', 'value1' : cp['pa_agreement_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['pa_agreement_cnt_(reconstruction)']},

                    {'label': 'PA Agreement', 'value1' : cp['1st_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['1st_tranche_cnt_(reconstruction)']},

                    {'label': 'PA Agreement', 'value1' : cp['2nd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['2nd_tranche_cnt_(reconstruction)']},

                    {'label': 'PA Agreement', 'value1' : cp['3rd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['3rd_tranche_cnt_(reconstruction)']}
                ],

                'houses': {
                    'under_construction': cp['houses_under_construction_cnt'],
                    'completed': cp['houses_completed_cnt'],
                },

                'retrofitting_status': [
                    {'label': 'Total Eligible HHs', 'value1': cp['total_eligible_hhs_(retrofit)'], 'value2': 0},

                    {'label': 'PA Agreement', 'value1': cp['pa_agreement_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['pa_agreement_cnt_(retrofit)']},

                    {'label': 'PA Agreement', 'value1': cp['1st_tranche_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['1st_tranche_cnt_(retrofit)']},

                    {'label': 'PA Agreement', 'value1': cp['2nd_tranche_cnt_(retrofit)'],
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
                },
                'health_posts': {
                    'damaged': cp['health_posts_damaged_cnt'],
                    'under_construction': cp['health_posts_under_const_cnt'],
                },
            },

            # Status of construction materials
            # title in cm_table
            'construction_materials': {
                m : {'unit': 'mq', 'req_quantity': cp['%s_required_quantity' % m] , 'ava': cp['%s_availability' % m],
                     'cost': cp['%s_cost' % m]}
                for m in ['stone', 'aggregate', 'sand', 'timber', 'cement_ppc', 'cement_opc', 'rebar', 'tin', 'bricks']},

            # Workers and wages
            'work_wage': {v : cp[v] for v in ['types_of_workers_1', 'avg_wage_1', 'types_of_workers_2', 'avg_wage_2']},

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
                    'q': 'Why do some households need to return the first tranche of 50,000 NPRs? If I need to return the tranche, how do I do it?', # noqa
                    'a': 'On 6 September 2018, the NRA Steering Committee decided that earthquake affected households who received the housing reconstruction grant multiple times, from multiple sources, who have another house that was not damaged in the earthquake, or households that received the housing reconstruction grant by providing fake details must return the grant amount by 30 December 2018. Those who wish to return the grant amount can contact the relevant GMALI DLPIU Office or may contact NRA’s free phone helpline: 16660-01-72000 (NTC) 9801572111 (Ncell)'  # noqa
                },
            ],
        }

def generate():
    w = pd.read_excel(
        '/Users/ewanog/Documents/work/code/repos/humanitarian/hrrp/gp_auto/maps/data/profile_data_structure_template.xlsx',
        sheet_name='Profile Data', index_col=0, header=0)

    sht = w.drop(w.index[0:2])
    sht = sht.rename(columns=lambda x: x.strip('#'))

    for v in sht.index.values:
        print('running for %s' %v)
        cur_rep = report(v, sht)
        cur_rep.create_data()

        PdfDraft('%s.pdf' %v)\
            .draw(Page1(cur_rep.data))\
            .draw(Page2(cur_rep.data))

if __name__ == '__main__':
    generate()
