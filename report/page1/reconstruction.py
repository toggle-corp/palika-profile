from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr

from report.common.color import Color


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
            font='RobotoCondensed 7.5',
        ),
        Row(width='60%', height='70%').add(
            Text(
                text='{}'.format(v1),
                font='Roboto bold 5',
                width='{}%'.format(v1p),
                height='100%',
                bg_color=color,
                vertical_alignment=Text.MIDDLE,
                padding=Rect([0, 4, 0, 4]),
            ),
            Text(
                text='{}'.format(v2 if v2 else ''),
                font='Roboto bold 5',
                width='{}%'.format(v2p),
                height='100%',
                bg_color=Color.GRAY,
                vertical_alignment=Text.MIDDLE,
                alignment=Text.RIGHT,
                padding=Rect([0, 4, 0, 4]),
            ),
        )
    )


def ReconstructionStatus():
    data = [
        {
            'label': 'Total Eligible HHs',
            'value1': 7070,
            'value2': 0,
        },
        {
            'label': 'PA Agreement',
            'value1': 4900,
            'value2': 1234,
        },
        {
            'label': 'PA Agreement',
            'value1': 1000,
            'value2': 1342,
        },
        {
            'label': 'PA Agreement',
            'value1': 2300,
            'value2': 1200,
        },
        {
            'label': 'PA Agreement',
            'value1': 3900,
            'value2': 4567,
        },
    ]

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


def Houses():
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
                markup='<b>Under Construction</b>: {}'.format(1234),
                font='RobotoCondensed 7.5',
            ),
            Text(
                markup='<b>Completed</b>: {}'.format(1234),
                font='RobotoCondensed 7.5',
            )
        ),
    )


def RetrofitStatus():
    data = [
        {
            'label': 'Total Eligible HHs',
            'value1': 7070,
            'value2': 0,
        },
        {
            'label': 'PA Agreement',
            'value1': 4900,
            'value2': 1234,
        },
        {
            'label': 'PA Agreement',
            'value1': 1000,
            'value2': 1342,
        },
        {
            'label': 'PA Agreement',
            'value1': 2300,
            'value2': 1200,
        },
    ]
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


def Grievances():
    return Column(width='50%').add(
        Text(
            text='Grievances',
            color=Color.ACCENT,
            font='RobotoCondensed bold 9',
            margin=Rect([0, 0, 4, 0]),
        ),
        Text(
            markup='<b>Registered:</b> {}'.format(1038),
            font='RobotoCondensed 7.5',
        ),
        Text(
            markup='<b>Addressed:</b> {}'.format(971),
            font='RobotoCondensed 7.5',
        ),
    )


def NonCompliance():
    return Column(width='50%').add(
        Text(
            text='Non-compliances',
            color=Color.ACCENT,
            font='RobotoCondensed bold 9',
            margin=Rect([0, 0, 4, 0]),
        ),
        Text(
            markup='<b>Registered:</b> {}'.format('-'),
            font='RobotoCondensed 7.5',
        ),
        Text(
            markup='<b>Addressed:</b> {}'.format('-'),
            font='RobotoCondensed 7.5',
        ),
    )


def ReconstructionAndRetrofit():
    return Row(width='100%', padding=Rect(8)).add(
        Column(width='50%', padding=Rect([0, 8, 0, 2])).add(
            ReconstructionStatus(),
            Houses(),
        ),
        Column(width='50%', padding=Rect([0, 2, 0, 8])).add(
            RetrofitStatus(),
            Row(width='100%').add(
                Grievances(),
                NonCompliance(),
            ),
        )
    )
