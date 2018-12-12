from drafter.utils import Rect, Border
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text

from report.common.boiler import boil
from report.common.color import Color

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
            text='-'*300,
            color=Color.DARK_GREEN,
            font_family="Roboto Condensed",
            font_size=5,
            auto_scale=True,
        ),

def PoGroup(data, **kwargs):
    print(**kwargs)
    return Column(
        height='50%',
        width='100%',
        border=Border(
            width=0.5,
            color=Color.BLACK,
        ),
    ).add(
        Text(
            width='100%',
            height='50%',
            text='| ' * 301,
            color=Color.DARK_GREEN,
            font_family="Roboto Condensed",
            font_size=5,
            auto_scale=True,
        ),
        Text(
            width='100%',
            height='50%',
            text='| '*301,
            color=Color.DARK_GREEN,
            font_family="Roboto Condensed",
            font_size=5,
            auto_scale=True,
        ),
    )

def Pop(data):
    return Column(width='100%', height='100%').add(
        Column(
            width='100% - 16',
            height='76%',
            margin=Rect([14, 8, 4, 8]),
        ).add(
            PoGroup(data)
        )
        .add(
            PoGroup(data)
        )
    )
