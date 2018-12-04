from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image
from report.common.color import Color


materials = [
    {'label': 'Stone', 'key': 'stone', 'icon': 'stone.png'},
    {'label': 'Aggregate', 'key': 'aggregate', 'icon': 'aggregate.png'},
    {'label': 'Sand', 'key': 'sand', 'icon': 'sand.png'},
    {'label': 'Timber', 'key': 'timber', 'icon': 'timber.png'},
    {'label': 'Cement (PPC)', 'key': 'cement_ppc', 'icon': 'cement.png'},
    {'label': 'Cement (OPC)', 'key': 'cement_opc', 'icon': 'cement.png'},
    {'label': 'Rebars', 'key': 'rebars', 'icon': 'rebar.png'},
    {'label': 'Tin', 'key': 'tin', 'icon': 'tin.png'},
    {'label': 'Bricks', 'key': 'bricks', 'icon': 'bricks.png'},
]


def xstr(item):
    if item == 'mq':
        return 'm<span rise="2000" size="x-small">3</span>'
    # TODO: Separate by comma if isinstance(item, int)
    return '{}'.format(item)


def TR_Text(widths, items):
    return Row(width='100%').add(
        *[
            Row(
                width=widths[i],
                height='100%',
                border=Border(
                    width=0.5,
                    color=Color.BLACK,
                ),
                padding=Rect(4),
            ).add(
                Text(
                    markup=xstr(item),
                    font='RobotoCondensed 6',
                    width=("100%" if i != 0 else None),
                    height="100%",
                    alignment=Text.CENTER,
                    vertical_alignment=Text.MIDDLE,
                )
            )
            for i, item in enumerate(items)
        ]
    )


def TR(widths, items):
    return Row(width='100%').add(
        *[
            Row(
                width=widths[i],
                height='100%',
                border=Border(
                    width=0.5,
                    color=Color.BLACK,
                ),
                padding=Rect([3, 0, 3, 0]),
            ).add(
                Image(
                    filename="resources/images/{}".format(item['icon']),
                    height=8,
                    margin=Rect(2),
                ) if item.get('icon') else None,
                Text(
                    markup=xstr(item.get('text')),
                    font='RobotoCondensed 6',
                    width=("100%" if i != 0 else None),
                    height="100%",
                    alignment=Text.CENTER,
                    vertical_alignment=Text.MIDDLE,
                )
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
            {'text': label, 'icon': material.get('icon')},
            {'text': datum['unit']},
            {'text': datum['req_quantity']},
            {'text': datum['ava']},
            {'text': datum['cost']},
        ])

    headers = ['<b>{}</b>'.format(k) for k in [
        'Materials', 'Unit', 'Req. Quantity*', 'Ava.', 'Cost. (NRS.)**',
    ]]
    widths = ['25%', '15%', '25%', '10%', '25%']

    return Column(width='100%', padding=Rect([16, 14, 0, 14])).add(
        TR_Text(widths=widths, items=headers),
        *[
            TR(widths=widths, items=row)
            for row in rows
        ],
        BottomBox(),
    )
