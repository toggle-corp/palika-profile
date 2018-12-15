from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text
from drafter.shapes import Pango

from report.common.color import Color
from report.common.utils import fmt_num
from report.common.boiler import boil

def TechnicalStaffFooter(**kwargs):
    return Text(
        **kwargs,
        text=boil('tech_staff_footer'),
        font_family='Roboto Condensed Light',
        font_size=5,
    )

def TechnicalStaff(tech_data, mason_data):
    widths = ['35%', '30%', '35%']
    headers = [boil('tech_staff_staff_title'), boil('tech_staff_available_title'), boil('tech_staff_addl_req_title')]

    tech_data = [
        [boil(item['lookup']), fmt_num(item['available']), fmt_num(item['additional'])] for item in tech_data
        ]

    mason_data = [boil(mason_data['lookup']), mason_data['available'], mason_data['additional']]

    # mason_data = [mason_data['label'], 100, 300]

    header_row = Row(width='100%').add(
    *[
        Text(
                border=Border(width=0.5, color=Color.BLACK),
                text=item,
                width=widths[i],
                font_family='Roboto Condensed',
                font_size=6,
                font_weight=Pango.Weight.BOLD,
                padding=Rect(4),
                alignment=(
                    Text.LEFT
                    if i == 0
                    else Text.CENTER
                ),
            )
        for i, item in enumerate(headers)
        ]
    )

    #add non masons
    data_rows = [
        Row(width='100%').add(
            *[
                Text(
                    border=Border(width=0.5, color=Color.BLACK),
                    text=item,
                    width=widths[i],
                    font_family='Roboto Condensed',
                    font_size=6,
                    font_weight=Pango.Weight.BOLD,
                    padding=Rect(4),
                    alignment=(
                        Text.LEFT
                        if i == 0
                        else Text.CENTER
                    ),
                )
                for i, item in enumerate(row)
            ],
        )
        for row in tech_data
    ]

    #add masons
    data_rows.append(
        Row(width='100%').add(
        *[
            Text(
                border=Border(width=0.5, color=Color.BLACK),
                text=mason_data[0],
                width=widths[0],
                font_family='Roboto Condensed',
                font_weight=Pango.Weight.BOLD,
                font_size=6,
                padding=Rect(4),
                alignment=Text.LEFT,
            ),
            #TODO: make num nepali
            Column(
                    border=Border(width=0.5, color=Color.BLACK),
                    height='100%',
                    width=widths[1],).add(
                Text(
                    text='{} ({} {})'.format(fmt_num(mason_data[1][0]), 7, boil('tech_staff_days')),
                    font_family='Roboto Condensed',
                    font_size=5,
                    width='100%',
                    alignment=Text.CENTER,
                    padding=Rect([2,0,0,0]),
                    )
                ).add(
                Text(
                    text='{} ({})'.format(fmt_num(mason_data[1][1]), 50, boil('tech_staff_days')),
                    font_family='Roboto Condensed',
                    font_size=5,
                    width='100%',
                    alignment=Text.CENTER,
                )
            ),
            Column(
                border=Border(width=0.5, color=Color.BLACK),
                height='100%',
                width=widths[2])
                .add(
                    Text(
                        text='{} ({} {})'.format(fmt_num(mason_data[2][0]), 7, boil('tech_staff_days')),
                        font_family='Roboto Condensed',
                        font_size=5,
                        width='100%',
                        alignment=Text.CENTER,
                        padding=Rect([2, 0, 0, 0]),
                    )
                ).add(
                    Text(
                        text='{} ({} {})'.format(fmt_num(mason_data[2][1]), 50, boil('tech_staff_days')),
                        font_family='Roboto Condensed',
                        font_size=5,
                        width='100%',
                        alignment=Text.CENTER,
                    )
            ),
        ]
    ))
    #
    # Row(width=widths[1],
    #     border=Border(width=0.5, color=Color.BLACK),
    #     height='100%').add(
    #     Row(border=Border(width=0.5, color=Color.BLACK)).add(
    #         Text(
    #             text='xx22',
    #             font='RobotoCondensed bold 6',
    #             alignment=Text.CENTER,
    #         ),
    #     ).add(Row(border=Border(width=0.5, color=Color.BLACK)).add(
    #         Text(
    #             text='yy',
    #             font='RobotoCondensed 6',
    #         ),
    #     ),
    #     ),

    return Column(
        width='100%',
        padding=Rect(16),
    ).add(
        header_row,
        *data_rows,
    )
