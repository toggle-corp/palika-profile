from drafter.utils import Rect, Border
from drafter.layouts import Row
from drafter.nodes import Text
from report.common.color import Color


def empty(**kwargs):
    return None


def Panel(**kwargs):
    title = kwargs.pop('title', None)
    left_footer = kwargs.pop('left_footer', empty)
    right_footer = kwargs.pop('right_footer', empty)
    footer_data = kwargs.pop('footer_data', empty)

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
        left_footer(
            absolute=True,
            bottom=-12,
            left=0,
            data=footer_data,
        ),
        right_footer(
            absolute=True,
            bottom=-12,
            right=2,
            data=footer_data,
        ),
    )
