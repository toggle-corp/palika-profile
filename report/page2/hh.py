import math

from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text
from drafter.color import hx
from drafter.shapes import Pango

from report.common.color import Color
from report.common.utils import fmt_num
from report.common.boiler import boil

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

def HH(data):
    total = sum(data.values())

    # title
    items = [
        {'key': 'landless', 'label': boil('land_issues_landless'), 'color': hx('#ff6117')},
        {'key': 'no_land_certificates', 'label': boil('land_issues_no_land_certificates'), 'color': hx('#bf053d')},
        # noqa
        {'key': 'right_of_way', 'label': boil('land_issues_right_of_way'), 'color': hx('#7d0547')},
        {'key': 'affected_by_hep', 'label': boil('land_issues_affected_by_hep'), 'color': hx('#1e7a8c')},  # noqa
        {'key': 'smallplots', 'label': boil('land_issues_small_plots'), 'color': hx('#abd1b5')},
        {'key': 'guthi_land', 'label': boil('land_issues_guthi_land'), 'color': hx('#ffc202')},
    ]

    bars = []
    labels = []
    for item in items:
        key = item['key']
        value = data.get(key, 0)
        color = item['color']

        if value and not (math.isnan(value) or math.isnan(total)):
            bar = Text(
                bg_color=color,
                height=14,
                width='{}%'.format(value / total * 100),
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                text=fmt_num(value),
                color=Color.WHITE,
                font_family='Roboto Condensed',
                font_size=6.7,
                font_weight=Pango.Weight.BOLD,
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
