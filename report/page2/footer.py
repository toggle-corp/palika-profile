from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.color import Color


def Footer(data):
    faq_blocks = []
    for item in data:
        question = Text(
            width='100%',
            text='Q: {}'.format(item['q']),
            font='RobotoCondensed bold 6.5',
        )
        answer = Text(
            width='100%',
            text='Ans: {}'.format(item['a']),
            font='RobotoCondensed Light 6',
        )
        faq_blocks.append(question)
        faq_blocks.append(answer)

    return Column(
        width='100%',
        padding=Rect([16, 16, 6, 16]),
    ).add(
        *faq_blocks,
    )
