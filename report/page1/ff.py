import math

from drafter.nodes import Canvas
from drafter.color import alpha
from drafter.shapes import (
    Shape,
    Arc,
    Rectangle,
    String,
    Pango,
)

from report.common.utils import fmt_thou
from report.common.color import Color
from report.common.boiler import boil


class Bagel(Shape):
    data = []

    def render(self, ctx):
        grades = []
        alpha_value = 1 / (2 ** (len(self.data) - 1))
        title = None
        dmg_val = None

        for k,v in self.data.items():
            if k == 'd1' :
                title = boil('facts_and_figures_damage_grade_(1-2)')
                dmg_val = self.data['d1']
            elif k == 'd3' :
                title = boil('facts_and_figures_damage_grade_(1-2)')
                dmg_val = self.data['d3']

            grades.append({
                'label' : title,
                'value' : dmg_val,
                'color' : alpha(Color.ACCENT, alpha_value)
            })
            alpha_value *= 2

        total_val = sum([item['value'] for item in grades])
        last_angle = None

        w = self.w / 2 - 17
        h = self.h - 65
        center = [w/2 + 25, h/2 + 28]
        radius = min(w, h) / 2

        for item in grades:
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
                line_width=12,
                angle1=(last_angle + math.pi / 180),
                angle2=(angle - math.pi / 180),
            ).render(ctx)
            last_angle = angle

        x = self.w / 2 + 24
        y = 32
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
                pos=[x + 14, y - 5],
                markup='<small>{}</small>\n<b>{}</b>'.format(label, fmt_thou(value)),
                font_family='Roboto Condensed',
                font_size=11,
            ).render(ctx)

            y += 60

        String(
            pos=center,
            markup='<small>{}</small>\n{}<span rise="3800" size="xx-small" >2</span>'.format(boil('facts_and_figures_total'), fmt_thou(total_val)),
            font_family='Roboto Condensed',
            font_size=11,
            font_weight = Pango.Weight.BOLD,
            alignment=String.CENTER,
        ).repos_to_center(ctx).render(ctx)

        String(
            pos=[self.w / 2, self.h - 16],
            text=boil('facts_and_figures_status'),
            font_family='Roboto Condensed',
            font_size=10.5,
            font_weight = Pango.Weight.BOLD,
            color=Color.ACCENT,
        ).repos_to_center(ctx).render(ctx)


def FF(data):
    return Canvas(
        width='100%',
        height='100%',
        renderer=Bagel(data=data),
    )
