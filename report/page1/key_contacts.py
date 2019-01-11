from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.boiler import boil
from report.common.utils import is_nan

def Contact(it, title, contact):

    #TODO: general handle
    for k,v in contact.items():
        if is_nan(v) or v == 'nan':
            contact[k] = '-'

    return Column(width = '100%', padding = Rect([0,8,0,8])).add(
        Text(
            text=title,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
        ),
        Text(
            text=contact['name'],
            font_family="Roboto Condensed",
            font_size=7,
        ),
        Text(
            text=contact['title'],
            font_family="Roboto Condensed",
            font_size=7,
        ),
        Text(
            text=contact['contact'],
            font_family="Roboto Condensed",
            font_size=7,
        )

    )


def KeyContacts(data):
    titles = [boil('key_contacts_municipal_office_title')]*4 + [boil('key_contacts_gmali/nra_title'),
                        boil('key_contacts_dlpiu-building_title')]

    return Column(margin=Rect([0,0,0,5])).add(Row(
        width='100%',
        padding=Rect([15, 0, 20, 0]),
    ).add(*[Contact(i, titles[i], contact) for i, contact in enumerate(data[:3])])).add(
     Row(
        width='100%',
        padding=Rect([0, 0, 12, 0]),
    ).add(*[Contact(i+3, titles[i+3], contact) for i, contact in enumerate(data[3:])]))
