import math

from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text
from drafter.color import hx
from drafter.shapes import Pango

from report.common.color import Color
from report.common.utils import fmt_num, get_text_width, nan_list_conv
from report.common.boiler import boil
import report.report

def _text_fits(txt, font_size, font, font_weight, cur_w):
    """see if text can fit in the rect w/ spacing"""
    # TODO: get actual width as opposed to manually specifying incase it changes
    TOTAL_W = 555
    rel_w = TOTAL_W * (cur_w/100)

    return rel_w > (get_text_width(txt, font_size, font, 'bold') + 2)

def Label(label, color):
    return Row(
        margin=Rect([8, 0, 0, 0]),
    ).add(
        Node(
            width=10,
            height=10,
            bg_color=color,
            margin=Rect([2, 4, 0, 0]),
        ),
        Text(
            text=label,
            font='Roboto Light 8',
            padding=Rect([2.5,0,0,0])
        )
    )

def HH(data):
    """for showing the HH bar. logic:
            if 0 values: show message that there are no reported issues
            if 1 value: do something #TODO
            else: show bar
            """
    total = sum(nan_list_conv(data.values(), 0))

    # title
    items = [
        {'key': 'landless', 'label': boil('land_issues_landless'), 'color': hx('#ff6117')},
        {'key': 'no_land_certificates', 'label': boil('land_issues_no_land_certificates'), 'color': hx('#bf053d')}, # noqa
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

        if value and not (math.isnan(value) or value == 0):
            cur_w = value / total * 100
            txt_ok = _text_fits(fmt_num(value), 11, 'Roboto Condensed', 'bold', cur_w)

            bar = Text(
                bg_color=color,
                height=20,
                width='{}%'.format(cur_w),
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                text=fmt_num(value) if txt_ok else '',
                color=Color.WHITE,
                font_family='Roboto Condensed',
                font_size=11,
                font_weight=Pango.Weight.BOLD,
            )
            bars.append(bar)

            label = Label(
                label=item['label'],
                color=color,
            )
            labels.append(label)

    if total == 0:
        return Column(width='100%', height='100%').add(
            Text(
                height='100%',
                width='100%',
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                text=boil('land_issues_no_information'),
                color=Color.GRAY,
                font_family='Roboto Condensed',
                font_size=18,
                font_weight=Pango.Weight.BOLD,
                margin=Rect([0,0,43,0]),
        )
    )

    else:
        return Column(
            width='100%',
            padding=Rect([16, 16, 8, 16]),
        ).add(
            Row(width='100%').add(*bars),
            Row(width='100%', justify='space-between' if len(labels) > 1 else None).add(*labels),
    )
