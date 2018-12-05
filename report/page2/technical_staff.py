from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text
from report.common.color import Color


def TechnicalStaffFooter(**kwargs):
    return Text(
        **kwargs,
        text='Source: Municipal Survey',
        font='RobotoCondensed light 5',
    )


def TechnicalStaff(data):
    widths = ['35%', '30%', '35%']
    headers = ['Staff', 'Available Nos.', 'Additional Req. Nos.']

    data = [
        [item['label'], item['available'], item['additional']]
        for item in data
    ]

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
        for row in data
    ]

    return Column(
        width='100%',
        padding=Rect(16),
    ).add(
        header_row,
        *data_rows,
    )
