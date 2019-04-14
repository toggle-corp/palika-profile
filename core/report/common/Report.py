from collections import OrderedDict

from ..common.utils import get_faq
from ..common.utils import get_resource_abspath
from ..common.boiler import boil_header, get_lang


class Report(object):
    def __init__(self, gc, data_sht, faq_sht, map_img_type):
        self.data_sht = data_sht
        self.faq_sht = faq_sht
        self.map_img_type = map_img_type

        self.gc = gc

    def create_data(self):
        """properly format input data according to sections. boiler.boil() is not used here but instead in the helper
            functions. boiler.boil_header() is used here, however, as it refers to dynamic content"""
        cp = self.data_sht.loc[self.gc]

        self.data = {
            # Date
            'rep_data': {
                'dist_nm': cp[boil_header('district_name')],
                'palika_nm': cp[boil_header('palika_name')],
            },

            # Facts and figures
            # title
            'facts_and_figures': {
                'd1': cp['damage_grade_1-2_cnt'],
                'd3': cp['damage_grade_3-5_cnt']
            },

            # Major Housing Typologies
            # very hacky work around with a lookup table as an iterator
            'housing_typologies':
                OrderedDict([
                    (
                        i[1], {
                            'muni_pct': cp['%s_municipal_pct' % i[0]],
                            'dist_pct': cp['%s_district_pct' % i[0]],
                        })
                    for i in [
                         ('stone_and_cement', 'typologies_stone_and_cement_mortar_masonry_row_title'), # noqa E501
                         ('stone_and_mud', 'typologies_stone_and_mud_mortar_masonry_row_title'), # noqa E501
                         ('brick_and_cement', 'typologies_brick_and_cement_mortar_masonry_row_title'), # noqa E501
                         ('brick_and_mud', 'typologies_brick_and_mud_mortar_masonry_row_title'), # noqa E501
                         ('rcc_frame', 'typologies_reinforced_cement_concrete_(rcc)_frame_row_title'), # noqa E501
                         ('hybrid', 'typologies_hybrid_structure_row_title'),
                         ('timber_frame', 'typologies_timber_frame_structure_row_title'), # noqa E501
                         ('hollow_concrete', 'typologies_hollow_concrete_block_masonry_row_title'), # noqa E501
                         ('dry_stone', 'typologies_dry_stone_masonry_row_title'), # noqa E501
                         ('adobe', 'typologies_adobe_structures_row_title'),
                         ('bamboo', 'typologies_bamboo_row_title'),
                         ('sceb', 'typologies_compressed_stabilized_earth_block_(sceb)_masonry_row_title'), # noqa E501
                         ('light_steel', 'typologies_light_steel_frame_structures_row_title')] # noqa E501
                ]),

            # Housing Reconstruction & Retrofit Updates
            'reconstruction_retrofit_updates': {
                'reconstruction_status': [
                    # title
                    {
                        'label': 'recon_&_retrofit_total_eligible_hhs_(both)',
                        'value1': cp['total_eligible_hhs_(reconstruction)'],
                        'value2': 0,
                    },
                    {
                        'label': 'recon_&_retrofit_pa_agreement_(both)',
                        'value1': cp['pa_agreement_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['pa_agreement_cnt_(reconstruction)'], # noqa E501
                    },
                    {
                        'label': 'recon_&_retrofit_ist_tranche_received_(both)', # noqa E501
                        'value1': cp['1st_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['1st_tranche_cnt_(reconstruction)'], # noqa E501
                    },
                    {
                        'label': 'recon_&_retrofit_iind_tranche_received_(both)', # noqa E501
                        'value1': cp['2nd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['2nd_tranche_cnt_(reconstruction)'], # noqa E501
                    },
                    {
                        'label': 'recon_&_retrofit_iiird_tranche_received',
                        'value1': cp['3rd_tranche_cnt_(reconstruction)'],
                        'value2': cp['total_eligible_hhs_(reconstruction)'] - cp['3rd_tranche_cnt_(reconstruction)'], # noqa E501
                    }
                ],

                'houses': {
                    'under_construction': cp['houses_under_construction_cnt'],
                    'completed': cp['houses_completed_cnt'],
                },

                'retrofitting_status': [
                    {
                        'label': 'recon_&_retrofit_total_eligible_hhs_(both)',
                        'value1': cp['total_eligible_hhs_(retrofit)'],
                        'value2': 0,
                    },
                    {
                        'label': 'recon_&_retrofit_pa_agreement_(both)',
                        'value1': cp['pa_agreement_cnt_(retrofit)'],
                        'value2': cp['total_eligible_hhs_(retrofit)'] - cp['pa_agreement_cnt_(retrofit)'], # noqa E501
                    },
                    {
                        'label': 'recon_&_retrofit_ist_tranche_received_(both)', # noqa E501
                        'value1': cp['1st_tranche_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['1st_tranche_cnt_(retrofit)'], # noqa E501
                    },
                    {
                        'label': 'recon_&_retrofit_iind_tranche_received_(both)', # noqa E501
                        'value1': cp['2nd_tranche_cnt_(retrofit)'],
                     'value2': cp['total_eligible_hhs_(retrofit)'] - cp['2nd_tranche_cnt_(retrofit)'], # noqa E501
                    },
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
                'po_presence_active': (cp[boil_header('active_pos_list')]),
                'po_presence_phased_out': (cp[boil_header('phased_out_pos_list')]),
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
                m: {
                    'req_quantity': cp['%s_required_quantity' % m],
                    'ava': cp[boil_header('%s_availability' % m)],
                    'cost': cp['%s_cost' % m]}
                for m in [
                        'stone', 'aggregate', 'sand', 'timber', 'cement_ppc',
                        'cement_opc', 'rebar', 'tin', 'bricks',
                ]
            },

            # Workers and wages
            'work_wage': {v: cp[v] for v in ['avg_wage_1', 'avg_wage_2']},

            # Key contacts
            'key_contacts': [
                {
                    'name': cp[boil_header('%sname' % c)],
                    'title': cp[boil_header('%srole' % c)],
                    'contact': str(cp['%scontact' % c])
                } for c in [
                    'municipal_contact_%i_' % n for n in range(1, 5)
                ] + ['nra_gmali_contact_', 'dlpiu_contact_']
            ],

            # HHs with Land Issues
            'hhs': {
                'landless': cp['landless_cnt'],
                'right_of_way': cp['right_of_way_cnt'],
                'no_land_certificates': cp['no_land_cert_cnt'],
                'affected_by_hep': cp['hep_cnt'],
                'smallplots': cp['small_plots_cnt'],
                'guthi_land': cp['guthi_land_cnt'],
            },

            # Status of technical staff
            # title
            'technical_staff': [
                {
                    'lookup': 'tech_staff_engineers',
                    'available': cp['engineers_available_cnt'],
                    'additional': cp['engineers_reqd_cnt'],
                },
                {
                    'lookup': 'tech_staff_sub-engineers',
                    'available': cp['sub-engineers_available_cnt'],
                    'additional': cp['sub-engineers_reqd_cnt'],
                },
                {
                    'lookup': 'tech_staff_asst._sub-engineers',
                    'available': cp['asst_sub-engineers_available_cnt'],
                    'additional': cp['asst_sub-engineers_reqd_cnt'],
                }
            ],

            # Status of Masons
            'technical_staff_masons':
                {
                    'lookup': 'tech_staff_masons',
                     'available': [
                         cp['masons_7_day_available_cnt'],
                         cp['masons_50_day_available_cnt'],
                     ],
                     'additional': [
                         cp['masons_7_day_reqd_cnt'],
                         cp['masons_50_day_reqd_cnt'],
                     ]
                 },

            # Trainings
            'trainings': {
                'short': {
                    'reached': cp['short_training_reached_cnt'],
                    'reqd': cp['short_training_reqd_cnt'],
                },
                'vocational': {
                    'reached': cp['voc_training_reached_cnt'],
                    'reqd': cp['voc_training_reqd_cnt'],
                },
            },

            # TODO: delete after running?
            # MAP
            'map': {
                'map_uri': get_resource_abspath(
                    'mapfiles/map_tmp/%s.%s' % (self.gc, self.map_img_type)
                ),
                'default_map_uri': get_resource_abspath('images/no_map.svg'),
                'legend_uri': get_resource_abspath('images/map_legend.png'),
            },

            # FAQ
            'faq': [
                {
                    'q': get_faq(
                        cp['faq_number_%i' % i],
                        self.faq_sht,
                    )['q'],
                    'a': get_faq(
                        cp['faq_number_%i' % i],
                        self.faq_sht,
                    )['a']
                } for i in range(1, 3)
            ],

            # Further info
            'further_info': [
                {
                    'name': cp[boil_header('further_info_%i_name' % i)],
                    'title': cp[boil_header('further_info_%i_title' % i)],
                    'phone': cp['further_info_%i_number' % i],
                } for i in range(1, 4)
            ],
        }
