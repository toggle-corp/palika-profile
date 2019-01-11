import math

from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text
from drafter.color import hx
from drafter.shapes import Pango

from report.common.color import Color
from report.common.utils import fmt_num, get_text_width
from report.common.boiler import boil

BAR_FNT_SZ = 11
BAR_FNT = 'Roboto Condensed'
BAR_STYLE = 'bold'
TOTAL_W_BAR = 555
NUM_PADDING = 555*.02

def _rect_size(hh_cnt, font_size, font, font_weight, sum_total):
    """if overlap, return smallest possible width"""
    # TODO: get actual width as opposed to manually specifying incase it changes
    rel_w = TOTAL_W_BAR * (hh_cnt / sum_total)
    actual_w = get_text_width(fmt_num(hh_cnt), font_size, font, font_weight) + NUM_PADDING

    #if the box is too wide for its box - set at min
    if rel_w < actual_w:
        return actual_w, False
    else:
        return rel_w, True

def _get_widths(items):
    """get the appropriate widths, keeping in mind that small text will get larger boxes
        we assume no 0s are passed"""
    # #TODO: revert
    # for v in items:
    #     try:
    #         v['val'] = int(v['val'])
    #     except:
    #         pass

    total = sum(v['val'] for v in items)

    if total > 0:
        for v in items:
            v['w'], v['flex'] = _rect_size(v['val'], BAR_FNT_SZ, BAR_FNT, BAR_STYLE, total)

        #get width taken up by fixed width boxes and total sum of flex boxes
        len_variable = TOTAL_W_BAR - sum(v['w'] for v in items if not v['flex'])
        flex_sum = sum(v['w'] for v in items if v['flex'])

        #for flex items, convert them to the proper share of the flex values
        for v in items:
            if v['flex']:
                v['w'] = len_variable * (v['w']/ flex_sum)

        #convert lengths to percentages
        for v in items:
            v['w'] /= TOTAL_W_BAR / 100

        return items

    else:
        return None

def _filter_items(items, data):
    """filter items and add their vals"""
    keep = []
    for v in items:
        d_v = data[v['key']]

        # #TODO: revert with check
        # try:
        #     d_v = int(d_v)
        # except:
        #     pass

        if d_v and not math.isnan(d_v) and d_v > 0:
            v['val'] = data[v['key']]
            keep.append(v)

    return keep

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

    # info f.e type
    items = [
        {'key': 'landless', 'label': boil('land_issues_landless'), 'color': hx('#ff6117')},
        {'key': 'no_land_certificates', 'label': boil('land_issues_no_land_certificates'), 'color': hx('#bf053d')}, # noqa
        {'key': 'right_of_way', 'label': boil('land_issues_right_of_way'), 'color': hx('#7d0547')},
        {'key': 'affected_by_hep', 'label': boil('land_issues_affected_by_hep'), 'color': hx('#1e7a8c')},  # noqa
        {'key': 'smallplots', 'label': boil('land_issues_small_plots'), 'color': hx('#abd1b5')},
        {'key': 'guthi_land', 'label': boil('land_issues_guthi_land'), 'color': hx('#ffc202')},
    ]

    # add val and drop item if it's zero or invalid
    items = _filter_items(items, data)

    wdz = _get_widths(items)

    bars = []
    labels = []
    if wdz:
        for item in wdz:
            color = item['color']

            bar = Text(
                bg_color=color,
                height=20,
                width='{}%'.format(item['w']),
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                text=fmt_num(item['val']),
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

        return Column(
            width='100%',
            padding=Rect([16, 16, 8, 16]),
        ).add(
            Row(width='100%').add(*bars),
            Row(width='100%', justify='space-between' if len(labels) > 1 else None).add(*labels)
        )

    else:
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
