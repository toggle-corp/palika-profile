from drafter.utils import Rect
from drafter.layouts import Column

from report.common.color import Color
from report.header import Header
from report.page1.page import Page as Page1Content
from report.page2.page import Page as Page2Content
from report.common.boiler import set_lang

WIDTH = 595
HEIGHT = 842


def Page1(data, LANG):
    set_lang(LANG)
    return Column(
        width=WIDTH,
        height=HEIGHT,
        bg_color=Color.WHITE,
        padding=Rect(32),
    ).add(
        Header(data),
        Page1Content(data),
    )


def Page2(data, LANG):
    set_lang(LANG)
    return Column(
        width=WIDTH,
        height=HEIGHT,
        bg_color=Color.WHITE,
        padding=Rect(32),
    ).add(
        Page2Content(data),
    )
