from drafter.utils import Rect, Border
from drafter.layouts import Row, Column
from drafter.nodes import Text, Image

from report.common.color import Color


def LegendImage():
    return None
    # return Image(filename="")


def MapImage():
    return None


def Map(data):
    map_footer = \
        'Count of TA activities represents presence of any of the following:'\
        'Demonstration Construction; Door-to-Door Technical Assistance;'\
        'Community/Household reconstruction orientation;'\
        'Helpdesk/Technical support center; Short training for mason;'\
        'Vocational/On-the-job training for mason;'\
        'OR Reconstruction Committee Formation.'

    return Column(
        width='100%',
        padding=Rect([16, 12, 10, 12]),
    ).add(
        Column(
            width='100%',
            height=330,
            border=Border(
                width=0.5,
                color=Color.BLACK,
            )
        ).add(
            LegendImage(),
            MapImage(),
        ),
        Text(
            width='100%',
            text=map_footer,
            border=Border(
                width=0.5,
                color=Color.BLACK,
            ),
            font='Roboto 4.5',
            line_spacing=3,
            padding=Rect([0, 4, 2, 4]),
        ),
    )
