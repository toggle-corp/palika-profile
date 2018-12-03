from drafter.utils import Rect, Border
from drafter.layouts import Row
from drafter.nodes import Text
from report.common.color import Color


def Panel(*args, **kwargs):
    title = kwargs.pop('title', None)

    return Row(
        border=Border(
            color=Color.BLUE,
            radius=16,
            width=1,
        ),
        relative=True,
        margin=Rect([10, 5, 10, 5]),
        **kwargs,
    ).add(
        Text(
            text=title,
            absolute=True,
            font='RobotoCondensed bold 9',
            color=Color.BLUE,
            top=-6,
            left=10,
            bg_color=Color.WHITE,
            padding=Rect([0, 6, 0, 6]),
        ),
        *args,
    )
