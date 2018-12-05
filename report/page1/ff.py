import math

from drafter.nodes import Canvas
from drafter.color import alpha
from drafter.shapes import (
    Shape,
    Arc,
    Rectangle,
    String,
)
from report.common.utils import fmt_thou

from report.common.color import Color


class Bagel(Shape):
    data = []

    def render(self, ctx):
        grades = []
        alpha_value = 1 / (2 ** (len(self.data) - 1))
        for datum in self.data:
            grades.append({
                **datum,
                'color': alpha(Color.ACCENT, alpha_value)
            })
            alpha_value *= 2

        total_val = sum([item['value'] for item in grades])
        last_angle = None

        w = self.w / 2 - 32
        h = self.h - 82
        center = [w/2 + 32, h/2 + 32]
        radius = min(w, h) / 2

        for item in grades:
            label = item['label']
            value = item['value']
            color = item['color']

            value_in_radians = value / total_val * 2 * math.pi
            if last_angle is None:
                last_angle = -math.pi / 2.5 - value_in_radians / 2
            angle = last_angle + value_in_radians

            Arc(
                center=center,
                radius=radius,
                line_color=color,
                line_width=8,
                angle1=(last_angle + math.pi / 180),
                angle2=(angle - math.pi / 180),
            ).render(ctx)
            last_angle = angle

        x = self.w / 2 + 24
        y = 20
        for item in grades:
            label = item['label']
            value = item['value']
            color = item['color']

            Rectangle(
                pos=[x, y],
                size=[8, 8],
                color=color,
                line_width=0,
            ).render(ctx)

            String(
                pos=[x + 14, y - 10],
                markup='<small>{}</small>\n<b>{}</b>'.format(label, fmt_thou(value)),
                font='RobotoCondensed 8',
            ).render(ctx)

            y += 32

        String(
            pos=center,
            markup='<small>Total</small>\n{}'.format(fmt_thou(total_val)),
            font='RobotoCondensed bold 9',
            alignment=String.CENTER,
        ).repos_to_center(ctx).render(ctx)

        String(
            pos=[self.w / 2, self.h - 16],
            text='Damage Status - Private Structures',
            font='RobotoCondensed bold 9',
            color=Color.ACCENT,
        ).repos_to_center(ctx).render(ctx)


def FF(data):
    return Canvas(
        width='100%',
        height='100%',
        renderer=Bagel(data=data['data']),
    )
