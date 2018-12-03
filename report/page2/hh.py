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


items = [
    {'key': 'landless', 'label': 'Landless', 'color': hx('#ff6117')},
    {'key': 'no_land_certificates', 'label': 'No Land Certificates', 'color': hx('#bf053d')},  # noqa
    {'key': 'right_of_way', 'label': 'Right of way', 'color': hx('#7d0547')},
    {'key': 'affected_by_hep', 'label': 'Affected by HEP', 'color': hx('#1e7a8c')},  # noqa
    {'key': 'smallplots', 'label': 'Small plots', 'color': hx('#abd1b5')},
    {'key': 'guthi_land', 'label': 'Guthi land', 'color': hx('#ffc202')},
    {'key': 'no_info', 'label': 'No information', 'color': hx('#949499')},
]


def HH(data):
    total = sum(data.values())

    bars = []
    labels = []
    for item in items:
        key = item['key']
        value = data.get(key, 0)
        color = item['color']

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
            label=item['label'],
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
