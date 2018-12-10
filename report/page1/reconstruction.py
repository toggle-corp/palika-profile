from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr

from report.common.color import Color
from report.common.utils import fmt_thou
from report.common.boiler import boil

def TwoValueLineChart(data, color):
    v1 = data['value1']
    v2 = data['value2']

    total = v1 + v2
    v1p = v1 / total * 100
    v2p = 100 - v1p

    return Row(
        width='100%',
        height=16,
        margin=Rect([4, 0, 0, 0]),
    ).add(
        Text(
            width='40%',
            text=data['label'],
            font='RobotoCondensed Bold 7.5',
        ),
        Row(width='60%', height='70%').add(
            Text(
                text=fmt_thou(v1),
                font='Roboto bold 7',
                width='{}%'.format(v1p),
                height='100%',
                bg_color=color,
                vertical_alignment=Text.MIDDLE,
                padding=Rect([0, 4, 0, 4]),
                color=Color.WHITE,
            ),
            Text(
                text=fmt_thou(v2) if v2 else '',
                font='Roboto bold 7',
                width='{}%'.format(v2p),
                height='100%',
                bg_color=Color.GRAY,
                vertical_alignment=Text.MIDDLE,
                alignment=Text.RIGHT,
                padding=Rect([0, 4, 0, 4]),
                color=Color.WHITE,
            ),
        )
    )


def ReconstructionStatus(data):
    rows = [
        TwoValueLineChart(datum, color=Color.ACCENT)
        for datum in data
    ]

    return Column(width='100%').add(
        Text(
            text='Reconstruction Status',
            font='RobotoCondensed bold 9',
            color=Color.ACCENT,
        ),
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
        *rows,
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
    )


def Houses(data):
    return Column(width='100%').add(
        Text(
            text='Houses',
            font='RobotoCondensed bold 9',
            color=Color.ACCENT,
        ),
        Row(
            width='100%',
            justify='space-between',
            margin=Rect([0, 0, 3, 0]),
        ).add(
            Text(
                markup='<b>Under Construction</b>: {}'.format(
                    fmt_thou(data['under_construction'])
                ),
                font='RobotoCondensed 7.5',
            ),
            Text(
                markup='<b>Completed</b>: {}'.format(
                    fmt_thou(data['completed'])
                ),
                font='RobotoCondensed 7.5',
            )
        ),
    )


def RetrofitStatus(data):
    rows = [
        TwoValueLineChart(datum, color=Color.ACCENT2)
        for datum in data
    ]

    return Column(width='100%').add(
        Text(
            text='Retrofitting Status',
            font='RobotoCondensed bold 9',
            color=Color.ACCENT,
        ),
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
        *rows,
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
    )


def Grievances(data):
    return Column(width='50%').add(
        Text(
            text='Grievances',
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([0, 0, 4, 0]),
        ),
        Text(
            markup='<b>Registered:</b> {}'.format(fmt_thou(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
        Text(
            markup='<b>Addressed:</b> {}'.format(fmt_thou(data['addressed'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def NonCompliance(data):
    return Column(width='50%').add(
        Text(
            text='Non-compliances',
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([0, 0, 4, 0]),
        ),
        Text(
            markup='<b>Registered:</b> {}'.format(fmt_thou(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
        Text(
            markup='<b>Addressed:</b> {}'.format(fmt_thou(data['addressed'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def ReconstructionAndRetrofit(data):
    return Row(width='100%', padding=Rect(8)).add(
        Column(width='50%', padding=Rect([0, 8, 0, 2])).add(
            ReconstructionStatus(data['reconstruction_status']),
            Houses(data['houses']),
        ),
        Column(width='50%', padding=Rect([0, 2, 0, 8])).add(
            RetrofitStatus(data['retrofitting_status']),
            Row(width='100%').add(
                Grievances(data['grievances']),
                NonCompliance(data['non_compliances']),
            ),
        )
    )
