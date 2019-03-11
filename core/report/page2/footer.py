from drafter.utils import Rect
from drafter.layouts import Column
from drafter.nodes import Text
from drafter.shapes import Pango

from ..common.boiler import boil


def Footer(data):
    faq_blocks = []
    for it, item in enumerate(data):
        question = Text(
            width='100%',
            text='{}: {}'.format(boil('faq_q'), item['q']),
            font_family='Roboto Condensed',
            font_size=8.5,
            font_weight=Pango.Weight.BOLD,
        )
        answer = Text(
            width='100%',
            text='{}: {}'.format(boil('faq_a'), item['a']),
            font_family='Roboto Condensed',
            font_size=8,
            padding=Rect([0, 0, 8, 0]) if it == 0 else Rect(0),
        )
        faq_blocks.append(question)
        faq_blocks.append(answer)

    return Column(
        width='100%',
        # padding=Rect([10, 16, 6, 16]),
    ).add(
        *faq_blocks,
    )
