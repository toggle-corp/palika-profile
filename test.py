from drafter.draft import PdfDraft
from report import Page1, Page2

"""
DUMMY DATA
"""

data = {
    # Facts and figures
    'facts_and_figures': {
        'data': [
            {'label': 'Damage Grade (1-2)', 'value': 7190},
            {'label': 'Damage Grade (3-5)', 'value': 4855},
        ],
    },

    # Major Housing Typologies
    'housing_typologies': {
        'headers': ['Typology', 'Municipal', 'District'],
        'data': [
            ['Bricks/Stone and Mud Mortar Masonry', '84.8%', '82%'],
            ['Bricks/Stone and Cement Mortar Masonry', '0.44%', '14%'],
            ['Other', '14.6%', '4%'],
        ],
    },

    # Housing Reconstruction & Retrofit Updates
    'reconstruction_retrofit_updates': {
        'reconstruction_status': [
            {'label': 'Total Eligible HHs', 'value1': 2842, 'value2': 0},
            {'label': 'PA Agreement', 'value1': 2352, 'value2': 490},
            {'label': 'PA Agreement', 'value1': 1000, 'value2': 1342},
            {'label': 'PA Agreement', 'value1': 288, 'value2': 2465},
            {'label': 'PA Agreement', 'value1': 300, 'value2': 500},
        ],

        'houses': {
            'under_construction': 123,
            'completed': 321,
        },

        'retrofitting_status': [
            {'label': 'Total Eligible HHs', 'value1': 217, 'value2': 0},
            {'label': 'PA Agreement', 'value1': 40, 'value2': 100},
            {'label': 'PA Agreement', 'value1': 70, 'value2': 130},
            {'label': 'PA Agreement', 'value1': 0, 'value2': 247},
        ],

        'grievances': {
            'registered': 683,
            'addressed': 681,
        },

        'non_compliances': {
            'registered': '-',
            'addressed': '-',
        },
    },

    # POs Presence
    'pos_presence': {
        'active': (
            'EcoH-N (Education, Health,'\
            'Social, Protection); NRCS (Health,'\
            'Housing, Livelihood, WASH,'\
            'Livestock)'
        ),
        'passive': (
            'AA (DRM, Edu., Livelihood, GESI);'\
            'ADRA, HELVETAS, NN, SABAL'\
            '(Housing); Garuda-N (Edu., WASH);'\
            'HI (DRM, Livelihood,Nutrition,'\
            'Housing); LWF (Livestock,'\
            'Livelihood, WASH); Tdh (Health)'
        ),
    },

    # Other Sectors
    'other_sectors': {
        'schools': {
            'damaged': '-',
            'under_construction': '-',
        },
        'health_posts': {
            'damaged': '-',
            'under_construction': '-',
        },
    },

    # Status of construction materials
    'construction_materials': {
        'stone': {'unit': 'msq', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'aggregate': {'unit': 'msq', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'sand': {'unit': 'msq', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'timber': {'unit': 'cu. ft.', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'cement_ppc': {'unit': 'sack', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'cement_opc': {'unit': 'sack', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'rebars': {'unit': 'kgs.', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'tin': {'unit': 'bundle', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
        'bricks': {'unit': 'pcs.', 'req_quantity': 97349, 'ava': 'Y', 'cost': 3000}, # noqa
    },

    # Key contacts
    'key_contacts': [
        {
            'office': 'Municipal Office',
            'name': 'Mr. Guman Dhoj Kunwar',
            'title': 'Chairperson',
            'contact': '98510123123',
        },
        {
            'office': 'Municipal Office',
            'name': 'Mr. Guman Dhoj Kunwar',
            'title': 'Chairperson',
            'contact': '98510123123',
        },
        {
            'office': 'Municipal Office',
            'name': 'Mr. Guman Dhoj Kunwar',
            'title': 'Chairperson',
            'contact': '98510123123',
        },
        {
            'office': 'Municipal Office',
            'name': 'Mr. Guman Dhoj Kunwar',
            'title': 'Chairperson',
            'contact': '98510123123',
        },
        {
            'office': 'Municipal Office',
            'name': 'Mr. Guman Dhoj Kunwar',
            'title': 'Chairperson',
            'contact': '98510123123',
        },
    ],

    # HHs with Land Issues
    'hhs': {
        'landless': 80,
        'right_of_way': 1405,
        'no_land_certificates': 325,
        'smallplots': 150,
        'guthi_land': 125,
    },

    # Status of technical staff
    'technical_staff': [
        {'label': 'engineers', 'available': '-', 'additional': '-'},
        {'label': 'sub_engineers', 'available': '-', 'additional': '-'},
        {'label': 'asst_sub_engineers', 'available': '-', 'additional': '-'},
        {'label': 'masons', 'available': '-', 'additional': '-'},
    ],

    # Trainings
    'trainings': {
        'short': {
            'reached': 370,
            'remaining': 47,
        },
        'vocational': {
            'reached': 20,
            'remaining': 591,
        },
    },

    # MAP
    'map': {},

    # FAQ
    'faq': [
        {
            'q': 'Why do some households need to return the first tranche of 50,000 NPRs? If I need to return the tranche, how do I do it?', # noqa
            'a': 'On 6 September 2018, the NRA Steering Committee decided that earthquake affected households who received the housing reconstruction grant multiple times, from multiple sources, who have another house that was not damaged in the earthquake, or households that received the housing reconstruction grant by providing fake details must return the grant amount by 30 December 2018. Those who wish to return the grant amount can contact the relevant GMALI DLPIU Office or may contact NRA’s free phone helpline: 16660-01-72000 (NTC) 9801572111 (Ncell)'  # noqa
        },
    ],
}

"""
END DUMMY DATA
"""


def generate():
    PdfDraft('test.pdf')\
        .draw(Page1(data))\
        .draw(Page2(data))


if __name__ == '__main__':
    generate()
