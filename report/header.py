from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr, Vr

from report.common.color import Color


def Header():
    return Column(
        width='100%',
        margin=Rect([0, 5, 8, 5]),
    ).add(
        Row(
            height=52,
        ).add(
            Text(
                text='Palika Profile',
                font='RobotoCondensed Bold 18',
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
                    text='November 2018',
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
