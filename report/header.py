from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image, Hr, Vr

from report.common.color import Color


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
                filename='resources/images/logo.png',
                width=96,
                absolute=True,
                top=-6,
                left=0,
            ),
            Text(
                text='Palika Profile',
                font='Roboto Condensed 18',
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
                    text='{} {}'.format(data['rep_data']['month'], data['rep_data']['year']),
                    font='Roboto Light 8',
                    color=Color.PRIMARY
                ),
                Text(
                    text='Kavrepalanchok | Banepa Municipality',
                    font='Roboto Light 15',
                    color=Color.PRIMARY
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
