from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text
from report.common.color import Color
from report.common.utils import fmt_thou

def TechnicalStaff(tech_data, mason_data):
    widths = ['35%', '30%', '35%']
    headers = ['Staff', 'Available Nos.', 'Additional Req. Nos.']

    tech_data = [
        [item['label'], fmt_thou(item['available']), fmt_thou(item['additional'])] for item in tech_data
    ]

    mason_data = [mason_data['label'], mason_data['available'], mason_data['additional']]

    # mason_data = [mason_data['label'], 100, 300]

    header_row = Row(width='100%').add(
    *[
        Text(
                border=Border(width=0.5, color=Color.BLACK),
                text=item,
                width=widths[i],
                font='RobotoCondensed bold 6',
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
                    font='RobotoCondensed 6',
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
                font='RobotoCondensed 6',
                padding=Rect(4),
                alignment=Text.LEFT,
            ),
            Column(
                    border=Border(width=0.5, color=Color.BLACK),
                    height='100%',
                    width=widths[1],).add(
                Text(
                    text='{} (7 days)'.format(fmt_thou(mason_data[1][0])),
                    font='RobotoCondensed 5',
                    width='100%',
                    alignment=Text.CENTER,
                    padding=Rect([2,0,0,0]),
                    )
                ).add(
                Text(
                    text='{} (50 days)'.format(fmt_thou(mason_data[1][1])),
                    font='RobotoCondensed 5',
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
                        text='{} (7 days)'.format(fmt_thou(mason_data[2][0])),
                        font='RobotoCondensed 5',
                        width='100%',
                        alignment=Text.CENTER,
                        padding=Rect([2, 0, 0, 0]),
                    )
                ).add(
                    Text(
                        text='{} (50 days)'.format(fmt_thou(mason_data[2][1])),
                        font='RobotoCondensed 5',
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
