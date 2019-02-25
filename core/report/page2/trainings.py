import math

from drafter.utils import Rect
from drafter.layouts import Node, Row, Column
from drafter.nodes import Text, Canvas
from drafter.shapes import Shape, String, Pie, Pango, LineShape

from ..common.color import Color
from ..common.utils import fmt_num
from ..common.boiler import boil


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
        padding=Rect([8, 10, 5, 10]),
    ).add(
        Node(
            width=7,
            height=7,
            bg_color=color,
            margin=Rect([0, 4, 0, 0]),
        ),
        Text(
            text=label,
            font='Roboto Light',
            font_size=6,
        )
    )


class PieChart(Shape):
    label = ''
    items = []

    def render(self, ctx):
        String(
            pos=[self.w/2, 0],
            text=self.label,
            font='Roboto Light',
            font_size=7,
            alignment=Text.CENTER,
        ).repos_to_center(ctx).render(ctx)

        pie_center = [self.w/2, self.h/2 + 9]
        radius = min(self.w/2, self.h/2)
        last_angle = None

        total_val = sum(
            [
                item['value'] if item['value'] is not None else 0
                for item in self.items
            ]
        )

        # we need to draw numbers at the end so they're on top
        # - store them in this array then render after pies
        nums = []

        # TODO: more graceful
        if total_val > 0:
            for it, item in enumerate(self.items):
                value = item['value']
                color = item['color']

                value_in_radians = value / total_val * 2 * math.pi
                if last_angle is None:
                    last_angle = -math.pi / 2.5 - value_in_radians / 2

                angle = last_angle + value_in_radians

                # don't show outline if very small sliver
                pct_cov = value / total_val
                if pct_cov != 0:
                    if .05 < pct_cov < .95:
                        l_w = 1

                    else:
                        l_w = 0

                    pie = Pie(
                        center=pie_center,
                        radius=radius,
                        color=color,
                        # only give an outline line if we have more than 10 pct
                        # (so we don't have white sliver
                        line_width=l_w,
                        line_color=Color.WHITE,
                        angle1=(last_angle),
                        angle2=(angle),
                    )
                    pie.render(ctx)
                    last_angle = angle

                    num_pos = pie.calc_center()
                    if pct_cov < .05:
                        num_pos[0] += 7

                    nums.append(
                        String(
                            pos=num_pos,
                            text=fmt_num(value),
                            font_family='Roboto Condensed',
                            font_size=5,
                            line_cap=LineShape
                        )
                    )

            for v in nums:
                if len(nums) == 1:
                    nums[0].pos = pie.calc_central_point(1)

                v.repos_to_center(ctx).render(ctx)

        # SlantedLine(
        #     p1 = [pie_center[0], pie_center[1] - radius],
        #     p2 = [25, -2],
        #     pct_cut = .08,
        #     rel_move = True,
        #     line_cap = LineShape.CAP_SQUARE,
        #     line_color = Color.ORANGE,
        #     # line_dash = [2,2],
        #     line_width = .5
        # ).render(ctx)


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
            height=13,
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
