from math import ceil

from drafter.utils import Rect, Border
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text

from report.common.boiler import boil
from report.common.color import Color
from report.common.utils import get_text_width, is_nan

def sand():
    t =         Text(
            width='100%',
            height='50%',
            text='x',
            color=Color.DARK_GREEN,
            font_family="Roboto Condensed",
            font_size=5,
            auto_scale=True,
        ),
    b =         Text(
            width='100%',
            height='50%',
            text=''*300,
            color=Color.DARK_GREEN,
            font_family="Roboto Condensed",
            font_size=5,
            auto_scale=True,
        ),

def _calc_box_hs(data):
    """take in top and bottom POs and size the boxes accordingly. is pretty approximate and doesn't incorporate text wrapping.
        we know that there are max 8 rows to work with. scenarios:

        *both are < 4x RW or both are > 4x RW: as is
        *else: floor(width/RW) to get # of rows f.e PO type. ensure min is met of smaller, then give space to other

    """
    #TODO: auto fit etc etc. make split rect shape?
    ROW_WIDTH = 235
    ROW_HEIGHT = 100/8 #quarter of a 100 pct box height
    NUM_ROWS = 8

    #TODO: change out for checking @ start

    a_r = ceil(get_text_width(data[0], 7, 'Roboto Condensed', 'normal')/ROW_WIDTH)
    p_r = ceil(get_text_width(data[1], 7, 'Roboto Condensed', 'normal')/ROW_WIDTH)

    a_nr = 4
    p_nr = 4

    if a_r <= 4 and p_r <= 4 or a_r >= 4 and p_r >= 4:
        pass

    else:
        if a_r < p_r:
            a_nr = max(1, a_r)
            p_nr = max(1, NUM_ROWS - a_nr)

        else:
            p_nr = max(1, p_r)
            a_nr = max(1, NUM_ROWS - p_nr)

    return (a_nr * ROW_HEIGHT, p_nr * ROW_HEIGHT)

def PoGroup(h, pos):
    #TODO: set global val for what blank is
    label = pos[0]
    pos_list = pos[1]

    return Column(
        width='98%',
        height='{}%'.format(h+4),
        border=Border(
            width=0.5,
            color=Color.BLACK,
        ),
    ).add(
        Text(
            width='98%',
            height='{}%'.format(h+4),
            # markup='{}'.format('hello '*60),
            markup='<b>{}:</b> {}'.format(boil(label), pos_list),
            color=Color.BLACK,
            font_family="Roboto Condensed",
            font_size=7,
            #TODO: fix bug where row cuts off early
            auto_scale_height=False,
            padding=Rect([1, 0, 5, 3]),
        ),
    )

def Pop(data):
    for k,v in data.items():
        if not v:
            data[k] = 'No POs Reported'

    hs = _calc_box_hs([v for v in data.values()])

    return Column(width='100%', height='100%').add(
        Column(
            width='100% - 16',
            height='76%',
            margin=Rect([12, 8, 4, 11]),
        ).add(
            *[PoGroup(info[0], info[1]) for info in zip(hs, data.items())]
        )
    )