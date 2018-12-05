from drafter.utils import Rect, Border
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text
from report.common.color import Color


def Label(label, color):
    return Row(
        padding=Rect(4),
    ).add(
        Node(
            width=10,
            height=10,
            bg_color=color,
            margin=Rect([0, 4, 0, 0]),
        ),
        Text(
            text=label,
            font='Roboto Light 6',
        )
    )


def Pop(data):
    return Column(width='100%', height='100%').add(
        Row(
            width='100% - 16',
            height='25% - 10',
            justify='end',
            margin=Rect([4, 8, 4, 8]),
        ).add(
            Label(label='Active', color=Color.DARK_GREEN),
            Label(label='Phased Out', color=Color.DARK_ORANGE),
        ),
        Row(
            width='100% - 16',
            height='75% - 10',
            margin=Rect([4, 8, 4, 8]),
        ).add(
            Text(
                width='50%',
                height='100%',
                border=Border(
                    width=0.5,
                    color=Color.BLACK,
                ),
                padding=Rect(4),
                text=data['active'],
                color=Color.DARK_GREEN,
                font='RobotoCondensed 5',
                auto_scale=True,
            ),
            Text(
                width='50%',
                height='100%',
                border=Border(
                    width=0.5,
                    color=Color.BLACK,
                ),
                padding=Rect(4),
                text=data['passive'],
                color=Color.DARK_ORANGE,
                font='RobotoCondensed 5',
                auto_scale=True,
            ),
        )
    )
