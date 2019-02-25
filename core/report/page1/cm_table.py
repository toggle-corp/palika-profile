from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image
from drafter.shapes import Pango

from ..common.color import Color
from ..common.utils import fmt_num
from ..common.boiler import boil
from ..common.utils import get_resource_abspath


def xstr(item):
    # TODO: nepali
    if item == 'm3':
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
                padding=Rect(5),
            ).add(
                Text(
                    markup=xstr(item),
                    font_family='Roboto Condensed',
                    font_size=7,
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
                padding=Rect([3, 6, 3, 0])
                if i in (2, 4) else Rect([3, 0, 3, 0]),
            ).add(
                Image(
                    filename=get_resource_abspath(
                        'images/{}'.format(item['icon']),
                    ),
                    height=8,
                    margin=Rect([2, 4, 4, 4]),
                ) if item.get('icon') else None,
                Text(
                    markup=xstr(item.get('text')),
                    font_family='Roboto Condensed',
                    font_size=7,
                    width=("100%" if i != 0 else None),
                    height="100%",
                    alignment=Text.RIGHT if i in (2, 4) else Text.CENTER,
                    vertical_alignment=Text.MIDDLE,
                )
            )
            for i, item in enumerate(items)
        ]
    )


def BottomBox(data):
    return Row(
        width='100%',
        margin=Rect([8, 0, 6, 0]),
        border=Border(
            width=0.5,
            color=Color.BLACK,
        ),
        padding=Rect([2, 8, 4, 8]),
    ).add(
        Column(width='50%').add(
            Text(
                text=boil('status_of_cm_types_of_workers'),
                font_family='Roboto Condensed',
                font_size=8,
                font_weight=Pango.Weight.BOLD,
            ),
            Text(
                text='{} {}'.format(
                    boil('status_of_cm_list_1'),
                    boil('status_of_cm_skilled_mason'),
                ),
                font_family='Roboto Condensed',
                font_size=8,
                padding=Rect([2, 0, 2, 0])
            ),
            Text(
                text='{} {}'.format(
                    boil('status_of_cm_list_2'),
                    boil('status_of_cm_labourer'),
                ),
                font_family='Roboto Condensed',
                font_size=8,
            ),
        ),
        Column(width='60%').add(
            Text(
                text=boil('status_of_cm_avg._daily_wage_(nrs.)'),
                width='100%',
                alignment=Text.CENTER,
                font_family='Roboto Condensed',
                font_size=8,
                font_weight=Pango.Weight.BOLD,
            ),
            Text(
                text='%s %s' % (fmt_num(data['avg_wage_1']), '/-'),
                width='65%',
                alignment=Text.RIGHT,
                font_family='Roboto Condensed',
                font_size=8,
                padding=Rect([2, 0, 2, 0]),
            ),
            Text(
                text='%s %s' % (fmt_num(data['avg_wage_2']), '/-'),
                width='65%',
                alignment=Text.RIGHT,
                font_family='Roboto Condensed',
                font_size=8,
                padding=Rect([0, 0, 1, 0]),
            )
        ),
    )


def CMTable(top_data, bot_data):
    materials = [
        {
            'label': boil('status_of_cm_stone'),
            'key': 'stone',
            'icon': 'stone.png',
            'unit': boil('status_of_cm_cubic_metre_measurement'),
        },
        {
            'label': boil('status_of_cm_aggregate'),
            'key': 'aggregate',
            'icon': 'aggregate.png',
            'unit': boil('status_of_cm_cubic_metre_measurement'),
        },
        {
            'label': boil('status_of_cm_sand'),
            'key': 'sand',
            'icon': 'sand.png',
            'unit': boil('status_of_cm_cubic_metre_measurement'),
        },
        {
            'label': boil('status_of_cm_timber'),
            'key': 'timber',
            'icon': 'timber.png',
            'unit': boil('status_of_cm_cubic_feet_measurement'),
        },
        {
            'label': boil('status_of_cm_cement_(ppc)'),
            'key': 'cement_ppc',
            'icon': 'cement.png',
            'unit': boil('status_of_cm_sack_measurement'),
        },
        {
            'label': boil('status_of_cm_cement_(opc)'),
            'key': 'cement_opc',
            'icon': 'cement.png',
            'unit': boil('status_of_cm_sack_measurement'),
        },
        {
            'label': boil('status_of_cm_rebars'),
            'key': 'rebar',
            'icon': 'rebar.png',
            'unit': boil('status_of_cm_kg_plural_measurement'),
        },
        {
            'label': boil('status_of_cm_tin'),
            'key': 'tin',
            'icon': 'tin.png',
            'unit': boil('status_of_cm_bundle_measurement'),
        },
        {
            'label': boil('status_of_cm_bricks'),
            'key': 'bricks',
            'icon': 'bricks.png',
            'unit': boil('status_of_cm_pieces_measurement'),
        }
    ]

    rows = []
    for material in materials:
        key = material['key']
        datum = top_data[key]
        label = material['label']

        if datum['ava'] is None:
            datum['ava'] = '-'

        rows.append([
            {'text': label, 'icon': material.get('icon')},
            {'text': material['unit']},
            {'text': fmt_num(datum['req_quantity'])},
            {'text': datum['ava']},
            {'text': fmt_num(datum['cost'])},
        ])

    headers = ['<b>{}</b>'.format(boil(k)) for k in [
        'status_of_cm_materials_header', 'status_of_cm_unit_header',
        'status_of_cm_req._quantity*_header',
        'status_of_cm_ava._header', 'status_of_cm_cost_(nrs.)**_header',
    ]]

    widths = ['28%', '12%', '25%', '10%', '25%']
    return Column(width='100%', padding=Rect([16, 14, 0, 14])).add(
        TR_Text(widths=widths, items=headers),
        *[
            TR(widths=widths, items=row)
            for row in rows
        ],
        BottomBox(bot_data),
    )
