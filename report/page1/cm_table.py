from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text
from report.common.color import Color


materials = [
    {'label': 'Stone', 'key': 'stone', 'icon': ''},
    {'label': 'Aggregate', 'key': 'aggregate', 'icon': ''},
    {'label': 'Sand', 'key': 'sand', 'icon': ''},
    {'label': 'Timber', 'key': 'timber', 'icon': ''},
    {'label': 'Cement (PPC)', 'key': 'cement_ppc', 'icon': ''},
    {'label': 'Cement (OPC)', 'key': 'cement_opc', 'icon': ''},
    {'label': 'Rebars', 'key': 'rebars', 'icon': ''},
    {'label': 'Tin', 'key': 'tin', 'icon': ''},
    {'label': 'Bricks', 'key': 'bricks', 'icon': ''},
]


def xstr(item):
    # TODO: Separate by comma if isinstance(item, int)
    return '{}'.format(item)


def TR(widths, items):
    return Row(width='100%').add(
        *[
            Text(
                width=widths[i],
                markup=xstr(item),
                font='RobotoCondensed 6',
                alignment=Text.CENTER,
                vertical_alignment=Text.MIDDLE,
                height='100%',
                border=Border(
                    width=0.5,
                    color=Color.BLACK,
                ),
                padding=Rect([3, 0, 3, 0]),
            )
            for i, item in enumerate(items)
        ]
    )


def BottomBox():
    return Row(
        width='100%',
        margin=Rect([8, 0, 6, 0]),
        border=Border(
            width=0.5,
            color=Color.BLACK,
        ),
        padding=Rect([1, 8, 4, 8]),
    ).add(
        Column(width='50%').add(
            Text(
                text='Types of workers',
                font='RobotoCondensed bold 6',
            ),
            Text(
                text='1. Skilled mason',
                font='RobotoCondensed 6',
            ),
            Text(
                text='2. Skilled mason',
                font='RobotoCondensed 6',
            )
        ),
        Column(width='50%').add(
            Text(
                text='Avg. daily wage (NRs.)',
                width='100%',
                alignment=Text.CENTER,
                font='RobotoCondensed bold 6',
            ),
            Text(
                text='1200/-',
                width='100%',
                alignment=Text.CENTER,
                font='RobotoCondensed 6',
            ),
            Text(
                text='950/-',
                width='100%',
                alignment=Text.CENTER,
                font='RobotoCondensed 6',
            )
        ),
    )


def CMTable(data):
    rows = []
    for material in materials:
        key = material['key']
        datum = data[key]
        label = material['label']

        rows.append([
            label,
            datum['unit'],
            datum['req_quantity'],
            datum['ava'],
            datum['cost'],
        ])

    headers = ['<b>{}</b>'.format(k) for k in [
        'Materials', 'Unit', 'Req. Quantity*', 'Ava.', 'Cost. (NRS.)**',
    ]]
    widths = ['25%', '15%', '25%', '10%', '25%']

    return Column(width='100%', padding=Rect([16, 14, 0, 14])).add(
        TR(widths=widths, items=headers),
        *[
            TR(widths=widths, items=row)
            for row in rows
        ],
        BottomBox(),
    )
