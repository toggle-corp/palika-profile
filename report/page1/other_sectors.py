from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Canvas
from drafter.shapes import Circle
from report.common.color import Color


class IconRenderer:
    def render(self, ctx):
        Circle(
            center=[self.w / 2, self.h / 2],
            radius=28,
        ).render(ctx)


def Sector(label, items):
    return Column(
        width='50%',
        height='100%',
        justify='center',
        align='center',
    ).add(
        Canvas(
            width=56,
            height=56,
            renderer=IconRenderer(),
        ),
        Text(
            text=label,
            color=Color.ACCENT,
            margin=Rect(4),
            font='RobotoCondensed bold 8',
        ),
        *[
            Row().add(
                Text(
                    text='{}: '.format(key),
                    font='RobotoCondensed bold 6',
                ),
                Text(
                    text=value,
                    font='RobotoCondensed 6',
                )
            )
            for key, value in items.items()
        ]
    )


def OtherSectors(data):
    schools = data['schools']
    health_posts = data['health_posts']

    return Row(
        width='100%',
        height='100%',
    ).add(
        Sector(
            label='Schools',
            items={
                'Damaged': schools['damaged'],
                'Under-construction': schools['under_construction'],
            },
        ),
        Sector(
            label='Health Posts',
            items={
                'Damaged': health_posts['damaged'],
                'Under-construction': health_posts['under_construction'],
            },
        ),
    )
