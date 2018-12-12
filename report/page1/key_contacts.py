from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.boiler import boil


def Contact(contact):
    return Column().add(
        Text(
            text=contact['office'],
            font='RobotoCondensed bold 8',
            margin=Rect([0, 0, 5, 0]),
        ),
        Text(
            text=contact['name'],
            font='RobotoCondensed 6',
        ),
        Text(
            text=contact['title'],
            font='RobotoCondensed 6',
        ),
        Text(
            text=contact['contact'],
            font='RobotoCondensed 6',
        ),
    )


def KeyContacts(data):
    return Row(
        width='100% - 32',
        justify='space-between',
        margin=Rect(16),
    ).add(*[Contact(contact=contact) for contact in data])
