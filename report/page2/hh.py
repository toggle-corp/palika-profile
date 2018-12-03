from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text
from drafter.color import hx

from report.common.color import Color


def Label(label, color):
    return Row(
        margin=Rect([8, 0, 0, 0]),
    ).add(
        Node(
            width=8,
            height=8,
            bg_color=color,
            margin=Rect([2, 4, 0, 0]),
        ),
        Text(
            text=label,
            font='Roboto Light 6',
        )
    )


def HH():
    values = {
        'Landless': 80,
        'No Land Certificates': 1405,
        'Right of way': 325,
        'Affected by HEP': 0,
        'Small plots': 150,
        'Guthi land': 125,
        'No information': 0,
    }

    colors = {
        'Landless': hx('#ff6117'),
        'No Land Certificates': hx('#bf053d'),
        'Right of way': hx('#7d0547'),
        'Affected by HEP': hx('#1e7a8c'),
        'Small plots': hx('#abd1b5'),
        'Guthi land': hx('#ffc202'),
        'No information': hx('#949499'),
    }

    keys = colors.keys()
    total = sum(values.values())

    bars = []
    labels = []
    for key in keys:
        value = values.get(key)
        color = colors[key]
        if value:
            bar = Text(
                bg_color=color,
                height=14,
                width='{}%'.format(value / total * 100),
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                text='{}'.format(value),
                color=Color.WHITE,
                font='Roboto bold 6.7',
            )
            bars.append(bar)

        label = Label(
            label=key,
            color=color,
        )
        labels.append(label)

    return Column(
        width='100%',
        padding=Rect([16, 16, 8, 16]),
    ).add(
        Row(width='100%').add(*bars),
        Row(width='100%', justify='space-between').add(*labels),
    )
