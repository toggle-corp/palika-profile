from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image, Canvas

from report.common.color import Color
from report.common.boiler import boil


def Map(data):

    return Column(
        width='100%',
        padding=Rect([16, 12, 10, 12]),
    ).add(
        Column(
            width='100%',
            height=380,
            border=Border(
                width=0.5,
                color=Color.BLACK,
            )
        ).add(
        Image(
            filename=data['legend_uri'],
            width='35%',
            height='5%',
            padding=Rect([0, 0, 0, 5])
        )).add(
        Image(
            filename=data['map_uri'],
            default_filename=data['default_map_uri'],
            width='99%',
            height='95%',
            padding=Rect([0,0,3,5])
        )),
        Text(
            width='100%',
            text=boil('map_footer'),
            border=Border(
                width=0.5,
                color=Color.BLACK,
            ),
            font='Roboto 4.5',
            line_spacing=3,
            padding=Rect([2, 4, 2, 4]),
        ),
    )
