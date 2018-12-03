from drafter.utils import Rect
from drafter.layouts import Column

from report.common.color import Color
from report.header import Header
from report.page1.page import Page as Page1Content
from report.page2.page import Page as Page2Content


WIDTH = 595
HEIGHT = 842


def Page1():
    return Column(
        width=WIDTH,
        height=HEIGHT,
        bg_color=Color.WHITE,
        padding=Rect(32),
    ).add(
        Header(),
        Page1Content(),
    )


def Page2():
    return Column(
        width=WIDTH,
        height=HEIGHT,
        bg_color=Color.WHITE,
        padding=Rect(32),
    ).add(
        Header(),
        Page2Content(),
    )
