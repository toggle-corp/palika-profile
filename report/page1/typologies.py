from collections import OrderedDict

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
    #TODO: assert that we don't have duplicate keys?
    #flatten and add dict
    rows = get_list_typo(OrderedDict((boil(k), v) for k,v in data.items()), 5)
    for v in rows.items():
        print(v)

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
                        text=k if i==0 else fmt_pct(list(d_v.items())[i-1][1], pts = 2),
                        index=i,
                        padding=Rect([4.5, 0, 4.5, 0]),
                    )
                    # i, item in enumerate(d_v.values())
                    for i in range(len(d_v.values())+1)
                ]
            )
            for k, d_v in rows.items()
        ],
        Text(
                width='100%',
                #TODO: add to lib
                #TODO: anchor to bottom
                text='CBS damage assessment survey, 2011',
                font_family="Roboto Light",
                font_size=6,
                alignment=Text.RIGHT,
                color=Color.GRAY,
                padding=Rect([0,0,10,0])
            ),
        )