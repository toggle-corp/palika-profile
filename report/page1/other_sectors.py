from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Canvas
from drafter.shapes import Circle, Image, Shape
from report.common.color import Color
from report.common.utils import fmt_thou

class IconRenderer(Shape):
    def render(self, ctx):
        Circle(
            center=[self.w / 2, self.h / 2],
            radius=24,
        ).render(ctx)

        Image(
            filename=self.filename,
            width=self.w / 2,
            pos=[self.w / 2, self.h / 2],
            center=True,
            scale_uniform=True,
        ).render(ctx)


def Sector(label, items, icon):
    return Column(
        width='50%',
        height='100%',
        justify='center',
        align='center',
    ).add(
        Canvas(
            width=56,
            height=56,
            renderer=IconRenderer(filename=icon),
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
                'Damaged': fmt_thou(schools['damaged']),
                'Under-construction': fmt_thou(schools['under_construction']),
            },
            icon='resources/images/school.png',
        ),
        Sector(
            label='Health Posts',
            items={
                'Damaged': fmt_thou(health_posts['damaged']),
                'Under-construction': fmt_thou(health_posts['under_construction']),
            },
            icon='resources/images/hospital.png',
        ),
    )
