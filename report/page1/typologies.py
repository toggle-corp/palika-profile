from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr

from report.common.color import Color
from report.common.boiler import boil
from report.common.utils import fmt_pct, get_list_typo

def Item(index, **kwargs):
    if index == 0:
        return Text(
            font_family="Roboto Condensed",
            font_size=8,
            font_weight=Text.BOLD,
            alignment=Text.LEFT,
            **kwargs,
        )
    else:
        return Text(
            font="Roboto light 8",
            alignment=Text.RIGHT,
            **kwargs,
        )


def Typologies(data):
    widths = ['60%', '20%', '20%']
    headers = [
        boil('typologies_typology'), boil('typologies_municipal'), boil('typologies_district')
    ]
    #flatten and add dict
    rows = get_list_typo([[boil(v['nm_look']), v['muni_pct'], v['dist_pct']] for v in data], 5, 1)

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
                    font_size=9,
                    font_weight=Text.BOLD,
                    color=Color.ACCENT,
                    alignment=Text.LEFT if i == 0 else Text.RIGHT,
                )
                for i, header in enumerate(headers)
            ]
        ),

        Hr(
            width='100%',
            height=1,
            color=Color.PRIMARY,
            dash=[3],
            margin=Rect([3, 0, 3, 0]),
        ),

        *[
            Row(width='100%').add(
                *[
                    Item(
                        width=widths[i],
                        text=item if i==0 else fmt_pct(item, pts = 2),
                        index=i,
                        padding=Rect([4.5, 0, 4.5, 0]),
                    )
                    for i, item in enumerate(row)
                ]
            )
            for row in rows
        ]
    )
