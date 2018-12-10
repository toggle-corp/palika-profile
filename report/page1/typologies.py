from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr

from report.common.color import Color
from report.common.boiler import boil

def Item(index, **kwargs):
    if index == 0:
        return Text(
            font_family="Roboto Condensed",
            font_size=8,
            font_weight=Text.BOLD,
            alignment=Text.LEFT,
            **kwargs,
        )

    return Text(
        font="Roboto light 8",
        alignment=Text.CENTER,
        **kwargs,
    )


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
                    font_family="Roboto Condensed",
                    font_size=8,
                    font_weight=Text.BOLD,
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
                    Item(
                        width=widths[i],
                        text=item,
                        index=i,
                        padding=Rect([4, 0, 4, 0]),
                    )
                    for i, item in enumerate(row)
                ]
            )
            for row in rows
        ]
    )
