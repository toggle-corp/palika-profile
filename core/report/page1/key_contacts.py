from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text

from ..common.boiler import boil
from ..common import ZERO_DEFAULT
from ..common.utils import get_lang_num


def Contact(it, title, contact):

    for k, v in contact.items():
        # TODO: fix 'none'
        if not v or v == 'None':
            contact[k] = '-'

    return Column(width='33%', padding=Rect([0, 8, 0, 8])).add(
        Text(
            text=title,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
        ),
        Text(
            text=contact['name'] if contact['name'] != ZERO_DEFAULT else '',
            font_family="Roboto Condensed",
            font_size=7,
        ),
        Text(
            text=contact['title'] if contact['title'] != ZERO_DEFAULT else '',
            font_family="Roboto Condensed",
            font_size=7,
        ),
        Text(
            text=get_lang_num(contact['contact']) if contact['contact'] != ZERO_DEFAULT else '',
            font_family="Roboto Condensed",
            font_size=7,
        )
    )


def KeyContacts(data):
    titles = [
        boil('key_contacts_municipal_office_title')
    ]*4 + [
        boil('key_contacts_gmali/nra_title'),
        boil('key_contacts_dlpiu-building_title'),
    ]

    return Column(
        width='100%',
        margin=Rect([0, 5, 0, 0]),
    ).add(
        Row(
            width='100%',
            padding=Rect([15, 0, 20, 0]),
        ).add(*[
            Contact(i, titles[i], contact) for i, contact in enumerate(data[:3])
        ])
    ).add(
        Row(
            width='100%',
            padding=Rect([0, 0, 12, 0]),
         ).add(*[
             Contact(
                 i+3, titles[i+3], contact
             ) for i, contact in enumerate(data[3:])
         ])
    )
