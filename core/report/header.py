from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image, Hr, Vr
from drafter.nodes.text import Pango

from .common.color import Color
from .common.boiler import boil
from .common.utils import get_resource_abspath


def Header(data):

    return Column(
        width='100%',
        margin=Rect([0, 5, 8, 5]),
    ).add(
        Row(
            height=52,
            relative=True,
        ).add(
            Image(
                filename=get_resource_abspath('images/logo.png'),
                width=96,
                absolute=True,
                top=-6,
                left=0,
            ),
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
                        data['rep_data']['month'],
                        data['rep_data']['year'],
                    ),
                    font='Roboto Light',
                    font_size=10,
                    color=Color.PRIMARY,
                ),
                Text(
                    text='{} | {}'.format(
                        data['rep_data']['dist_nm'],
                        data['rep_data']['palika_nm'],
                    ),
                    font='Roboto Light',
                    font_size=18,
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
