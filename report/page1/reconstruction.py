from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr

from report.common.color import Color
from report.common.utils import fmt_num
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
            text=boil(data['label']),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
        ),
        Row(width='60%', height='70%').add(
            Text(
                text=fmt_num(v1),
                font='Roboto bold 8',
                width='{}%'.format(v1p),
                height='100%',
                bg_color=color,
                vertical_alignment=Text.MIDDLE,
                padding=Rect([0, 4, 0, 4]),
                color=Color.WHITE,
            ),
            Text(
                text=fmt_num(v2) if v2 else '',
                font='Roboto bold 8',
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
        #pass up label, v1, v2
        TwoValueLineChart(datum, color=Color.ACCENT)
        for datum in data
    ]

    return Column(width='100%').add(
        Text(
            text=boil('recon_&_retrofit_reconstruction_status_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
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
            margin=Rect([3, 0, 1, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
    )


def Houses(data):
    return Column(width='100%').add(
        Text(
            text=boil('recon_&_retrofit_houses_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            color=Color.ACCENT,
            margin=Rect([0, 0, 2, 0])
        ),
        Row(
            width='100%',
            justify='space-between',
            margin=Rect([0, 0, 3, 0]),
        ).add(
            Text(
                markup='<b>{}</b>: {}'.format(boil('recon_&_retrofit_under_construction'),
                                              fmt_num(data['under_construction'])
                                              ),
                font_family="Roboto Condensed",
                font_size=7.5,
            ),
            Text(
                markup='<b>{}</b>: {}'.format(boil('recon_&_retrofit_completed'),
                                              fmt_num(data['completed'])
                                              ),
                font_family="Roboto Condensed",
                font_size=7.5,
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
            text=boil('recon_&_retrofit_retrofitting_status_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
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
            text=boil('recon_&_retrofit_grievances_title'),
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([3.2, 0, 5, 0]),
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_registered_(both)'), fmt_num(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_addressed_(both)'), fmt_num(data['addressed'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def NonCompliance(data):
    return Column(width='50%').add(
        Text(
            text=boil('recon_&_retrofit_non-compliances_title'),
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([3.2, 0, 5, 0]),
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_registered_(both)'), fmt_num(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_addressed_(both)'), fmt_num(data['addressed'])),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def ReconstructionAndRetrofit(data):
    return Row(width='100%', padding=Rect(8)).add(
        Column(width='50%', padding=Rect([3, 8, 0, 2])).add(
            ReconstructionStatus(data['reconstruction_status']),
            Houses(data['houses']),
        ),
        Column(width='50%', padding=Rect([3, 2, 0, 8])).add(
            RetrofitStatus(data['retrofitting_status']),
            Row(width='100%').add(
                Grievances(data['grievances']),
                NonCompliance(data['non_compliances']),
            ),
        )
    )
