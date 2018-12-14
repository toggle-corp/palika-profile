from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.boiler import boil

# self.top = value[0]
# self.right = value[1]
# self.bottom = value[2]
# self.left = value[3]


def Contact(it, title, contact):
    t_pad = 12 if it < 3 else 10
    r_pad = 0
    b_pad = 8 if it > 3 else 0

    #to fix some weird error where bottom right wasn't properly spaced
    if it in (0,3):
        l_pad = 55
    elif it == 5:
        l_pad = 124.5
    else:
        l_pad = 120

    return Column().add(
        Text(
            text=title,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([t_pad, r_pad, 3, l_pad]),
        ),
        Text(
            text=contact['name'],
            font_family="Roboto Condensed",
            font_size=7,
            margin=Rect([0, 0, 0, l_pad]),
        ),
        Text(
            text=contact['title'],
            font_family="Roboto Condensed",
            font_size=7,
            margin=Rect([0, 0, 0, l_pad]),
        ),
        Text(
            text=contact['contact'],
            font_family="Roboto Condensed",
            font_size=7,
            margin=Rect([0, 0, b_pad, l_pad]),
        )

    )


def KeyContacts(data):
    titles = [boil('key_contacts_municipal_office_title')]*4 + [boil('key_contacts_gmali/nra_title'),
                        boil('key_contacts_dlpiu-building_title')]

    return Column().add(Row(
        width='100%',
    ).add(*[Contact(i, titles[i], contact) for i, contact in enumerate(data[:3])])).add(
     Row(
        width='100%',
    ).add(*[Contact(i+3, titles[i+3], contact) for i, contact in enumerate(data[3:])]))
