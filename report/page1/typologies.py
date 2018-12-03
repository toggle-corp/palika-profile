from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr
from report.common.color import Color


def Typologies(data):
    widths = ['60%', '20%', '20%']
    headers = data['headers']
    rows = data['data']

    return Column(
        width='100%',
        padding=Rect(12),
    ).add(
        Row(width='100%').add(
            *[
                Text(
                    width=widths[i],
                    text=header,
                    font='RobotoCondensed bold 8',
                    color=Color.ACCENT,
                    alignment=(
                        Text.LEFT
                        if i == 0
                        else Text.CENTER
                    )
                )
                for i, header in enumerate(headers)
            ]
        ),

        Hr(
            width='100%',
            height=1,
            color=Color.PRIMARY,
            dash=[3],
            margin=Rect([3, 0, 6, 0]),
        ),

        *[
            Row(width='100%').add(
                *[
                    Text(
                        width=widths[i],
                        text=item,
                        font=(
                            'RobotoCondensed bold 6'
                            if i == 0
                            else 'Roboto light 6'
                        ),
                        alignment=(
                            Text.LEFT
                            if i == 0
                            else Text.CENTER
                        ),
                        padding=Rect([2, 0, 2, 0]),
                    )
                    for i, item in enumerate(row)
                ]
            )
            for row in rows
        ]
    )
