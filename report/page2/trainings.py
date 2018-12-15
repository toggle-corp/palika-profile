import math

from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text, Canvas
from drafter.shapes import Shape, String, Pie, Pango

from report.common.color import Color
from report.common.utils import fmt_num
from report.common.boiler import boil


def TrainingsFooter(**kwargs):
    return Text(
        **kwargs,
        text=boil('training_footer'),
        font_family='Roboto Condensed Light',
        font_size=5,
    )


def Label(label, color):
    return Row(
        margin=Rect([0, 10, 0, 10]),
    ).add(
        Node(
            width=7,
            height=7,
            bg_color=color,
            margin=Rect([2, 4, 0, 0]),
        ),
        Text(
            text=label,
            font='Roboto Light 6',
        )
    )


class PieChart(Shape):
    label = ''
    items = []

    def render(self, ctx):
        String(
            pos=[self.w/2, 4],
            text=self.label,
            font='Roboto Light 7',
            alignment=Text.CENTER,
        ).repos_to_center(ctx).render(ctx)

        pie_center = [self.w/2, self.h/2 + 6]
        radius = min(self.w/2, self.h/2 - 6 )
        last_angle = None

        total_val = sum([item['value'] for item in self.items])

        for item in self.items:
            value = item['value']
            color = item['color']

            value_in_radians = value / total_val * 2 * math.pi
            if last_angle is None:
                last_angle = -math.pi / 2.5 - value_in_radians / 2
            angle = last_angle + value_in_radians

            pie = Pie(
                center=pie_center,
                radius=radius,
                color=color,
                line_width=1,
                line_color=Color.WHITE,
                angle1=(last_angle),
                angle2=(angle),
            )
            pie.render(ctx)
            last_angle = angle

            String(
                pos=pie.calc_center(),
                text=fmt_num(value),
                font_family='Roboto Condensed',
                font_size=5,
            ).repos_to_center(ctx).render(ctx)


def Trainings(data):
    short = data['short']
    vocational = data['vocational']

    short_training = [
        {'value': short['reached'], 'color': Color.ACCENT},
        {'value': short['remaining'], 'color': Color.GRAY},
    ]
    vocational_training = [
        {'value': vocational['reached'], 'color': Color.ACCENT},
        {'value': vocational['remaining'], 'color': Color.GRAY},
    ]

    items = [
        {'label': boil('training_reached'), 'color': Color.ACCENT},
        {'label': boil('training_remaining'), 'color': Color.GRAY},
    ]

    return Column(
        width='100%',
        height='100%',
        padding=Rect([10, 10, 4, 10]),
    ).add(
        Text(
            height=16,
            text=boil('training_sub_title'),
            color=Color.PRIMARY,
            font_family='Roboto Condensed',
            font_size=8,
            font_weight=Pango.Weight.BOLD,
        ),
        Row(width='100%', height='100% - 32', padding=Rect(4)).add(
            Canvas(
                width='50%',
                height='100%',
                renderer=PieChart(
                    items=short_training,
                    label=boil('training_short_training'),
                )
            ),
            Canvas(
                width='50%',
                height='100%',
                renderer=PieChart(
                    items=vocational_training,
                    label=boil('training_vocational_training'),
                )
            ),
        ),
        Row(
            width='100%',
            height=16,
            justify='center',
            align='center',
        ).add(
            *[
                Label(
                    label=item['label'],
                    color=item['color'],
                ) for item in items
            ]
        ),
    )
