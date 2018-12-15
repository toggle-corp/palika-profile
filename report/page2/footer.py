from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text
from drafter.shapes import Pango

from report.common.boiler import boil


def Footer(data):
    faq_blocks = []
    for item in data:
        question = Text(
            width='100%',
            text='{}: {}'.format(boil('faq_q'), item['q']),
            font_family='Roboto Condensed',
            font_size=6.5,
            font_weight=Pango.Weight.BOLD,
        )
        answer = Text(
            width='100%',
            text='{}: {}'.format(boil('faq_a'), item['a']),
            font_family='Roboto Condensed',
            font_size=6,
        )
        faq_blocks.append(question)
        faq_blocks.append(answer)

    return Column(
        width='100%',
        padding=Rect([16, 16, 6, 16]),
    ).add(
        *faq_blocks,
    )
