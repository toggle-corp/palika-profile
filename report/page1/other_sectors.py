from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text, Canvas
from drafter.shapes import Circle, Image, Shape, Pango

from report.common.color import Color
from report.common.utils import fmt_num
from report.common.boiler import boil

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
            font_family='Roboto Condensed',
            font_size=8,
            font_weight=Pango.Weight.BOLD,
        ),
        *[
            Row().add(
                Text(
                    text='{}: '.format(key),
                    font_family='Roboto Condensed',
                    font_size=8,
                    font_weight=Pango.Weight.BOLD,
                ),
                Text(
                    text=value,
                    font_family='Roboto Condensed',
                    font_size=8,
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
            label=boil('other_sectors_schools_title'),
            items={
                    boil('other_sectors_damaged'): fmt_num(schools['damaged']),
                    boil('other_sectors_under-construction'): fmt_num(schools['under_construction']),
                    boil('other_sectors_const._completed'): fmt_num(schools['const_comp']),
            },
            icon='resources/images/school.png',
        ),
        Sector(
            label=boil('other_sectors_health_posts_title'),
            items={
                boil('other_sectors_damaged'): fmt_num(health_posts['damaged']),
                boil('other_sectors_under-construction'): fmt_num(health_posts['under_construction']),
                boil('other_sectors_const._completed'): fmt_num(health_posts['const_comp']),
            },
            icon='resources/images/hospital.png',
        ),
    )
