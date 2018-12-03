from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.color import Color


def Footer():
    faq = [
        {
            'question': 'Why do some households need to return the first tranche of 50,000 NPRs? If I need to return the tranche, how do I do it?', # noqa
            'answer': 'On 6 September 2018, the NRA Steering Committee decided that earthquake affected households who received the housing reconstruction grant multiple times,'\
                'from multiple sources, who have another house that was not damaged in the earthquake, or households that received the housing reconstruction grant by providing'\
                'fake details must return the grant amount by 30 December 2018. Those who wish to return the grant amount can contact the relevant GMALI DLPIU Office or may'\
                'contact NRA’s free phone helpline: 16660-01-72000 (NTC) 9801572111 (Ncell)'
        },
    ]

    faq_blocks = []
    for item in faq:
        question = Text(
            width='100%',
            text='Q: {}'.format(item['question']),
            font='RobotoCondensed bold 6.5',
        )
        answer = Text(
            width='100%',
            text='Ans: {}'.format(item['answer']),
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
