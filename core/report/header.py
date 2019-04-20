from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr, Vr
from drafter.nodes.text import Pango

from .common.color import Color
from .common.boiler import boil
from .common.utils import get_text_width, get_lang_num

ADM_NM_WIDTH = 368
NM_FNT_SZ = 18


def calc_nm_len(txt):
    """
    hacky method to shrink titles. will break if absolute width of
    values changes or if font values change!!
    """
    txt_w = get_text_width(txt, NM_FNT_SZ, 'Roboto Light', 'normal')

    if txt_w > ADM_NM_WIDTH:
        return NM_FNT_SZ * (ADM_NM_WIDTH/txt_w)
    else:
        return NM_FNT_SZ


def Header(data):
    nm_text = '{} | {}'.format(
        data['rep_data']['dist_nm'],
        data['rep_data']['palika_nm'],
    )

    return Column(
        width='100%',
        margin=Rect([0, 5, 8, 5]),
    ).add(
        Row(
            height=52,
            width='10%'
        ).add(
            Text(
                text=boil('header_title'),
                font_family='Roboto Condensed',
                font_size=24,
                font_weight=Pango.Weight.BOLD,
                color=Color.PRIMARY,
                height='100%',
                vertical_alignment=Text.BOTTOM,
            ),
            Vr(
                width=2,
                height='100%',
                color=Color.PRIMARY,
                margin=Rect([0, 16, 0, 16]),
                padding=Rect([24, 0, 0, 0]),
            ),
            Column(height='100%', justify='end').add(
                Text(
                    text='{} {}'.format(
                        boil('header_month'),
                        boil('header_year') if isinstance(boil('header_year'), str) else get_lang_num(str(boil('header_year'))),
                    ),
                    font='Roboto Light',
                    font_size=10,
                    color=Color.PRIMARY,
                ),
                Text(
                    text=nm_text,
                    font='Roboto Light',
                    font_size=calc_nm_len(nm_text),
                    color=Color.PRIMARY,
                )
            )
        ),
        Hr(
            width='100%',
            height=1,
            color=Color.PRIMARY,
            margin=Rect([8, 0, 0, 0]),
        ),
        Hr(
            width='100%',
            height=1.8,
            color=Color.PRIMARY,
            margin=Rect([2, 0, 0, 0]),
        ),
    )
