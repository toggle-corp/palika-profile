from drafter.utils import Rect
from drafter.shapes import Shape, Rectangle, String
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr, Canvas
from drafter.shapes import Pango

from ..common import ZERO_DEFAULT
from ..common.color import Color
from ..common.utils import fmt_num, get_text_width
from ..common.boiler import boil, get_lang


class Bars(Shape):
    def __init__(self, data, bar_color):
        self.data = data
        self.bar_color = bar_color

    def _x_pos_v1(self):
        if (self.v1_len + self.NUM_PAD) > self.r1_w:
            self.inv_v1_col = True
            return self.r1_w + self.NUM_PAD
        else:
            return self.NUM_PAD

    def _x_pos_v2(self):
        if self.r2_w == 0:
            self.inv_v2_col = True
            return self.F_W - self.v2_len
        elif (self.v2_len + self.NUM_PAD) > self.r2_w:
            self.inv_v2_col = True
            return self.r1_w - self.v2_len - self.NUM_PAD
        else:
            return self.F_W - self.v2_len - self.NUM_PAD

    def _draw_regular_rect(self):
        font_family = 'Roboto'
        font_size = 8
        font_weight = Pango.Weight.BOLD

        self.v1_str = fmt_num(self.v1)
        self.v2_str = fmt_num(self.v2)

        if self.v1 == 0:
            self.v1_str = ''
        if self.v2 == 0:
            self.v2_str = ''

        self.inv_v1_col = False
        self.inv_v2_col = False

        self.v1_len = get_text_width(
            self.v1_str, font_size, font_family, 'bold',
        )
        self.v2_len = get_text_width(
            self.v2_str, font_size, font_family, 'bold',
        )

        self.r1_w = 0 if (self.v1 + self.v2) == 0\
            else (self.v1 / (self.v1 + self.v2)) * self.F_W
        self.r2_w = 0 if (self.v1 + self.v2) == 0\
            else (self.v2 / (self.v1 + self.v2)) * self.F_W

        # TODO: revert with full check

        from ..common.utils import is_nan
        if is_nan(self.r1_w):
            self.r1_w = 0
        if is_nan(self.r2_w):
            self.r2_w = 0

        if self.v1_str == ZERO_DEFAULT:
            self.v1_str = ''

        # end revert

        # v1 rect
        Rectangle(
            pos=[0, 0],
            size=[self.r1_w, self.RECT_HEIGHT],
            color=self.bar_color,
            line_width=0,
        ).render(self.ctx)

        # v2 rect
        Rectangle(
            pos=[self.r1_w, 0],
            size=[self.F_W - self.r1_w, self.RECT_HEIGHT],
            color=Color.GRAY,
            line_width=0,
        ).render(self.ctx)

        # v1 string
        String(
            pos=[self._x_pos_v1(), self.Y_PAD],
            markup=self.v1_str,
            font_family=font_family,
            font_size=font_size,
            font_weight=font_weight,
            color=Color.WHITE if not self.inv_v1_col else self.bar_color,
            alignment=String.LEFT,
        ).render(self.ctx)

        # v2 string
        String(
            pos=[self._x_pos_v2(), self.Y_PAD],
            markup=self.v2_str,
            font_family=font_family,
            font_size=font_size,
            font_weight=font_weight,
            color=Color.WHITE if not self.inv_v2_col else Color.GRAY,
            alignment=String.LEFT,
        ).render(self.ctx)

    def _draw_empty_rect(self):
        """for when there is zero values for both types"""
        font_family = 'Roboto'
        font_size = 8
        font_weight = Pango.Weight.BOLD

        Rectangle(
            pos=[0, 0],
            size=[self.F_W, self.RECT_HEIGHT],
            color=Color.WHITE,
            line_width=1,
            line_color=Color.LIGHT_GRAY,
        ).render(self.ctx)

        String(
            pos=[self.F_W/2, self.Y_PAD],
            markup=fmt_num(0),
            font_family=font_family,
            font_size=font_size,
            font_weight=font_weight,
            color=Color.BLACK,
        ).render(self.ctx)

    def render(self, ctx):
        self.ctx = ctx
        self.F_W = 148
        self.NUM_PAD = 2 if get_lang() == 'en' else 4
        self.Y_PAD = 1 if get_lang() == 'en' else 0
        self.RECT_HEIGHT = 12

        # TODO: logic?

        self.v1 = self.data['value1']
        self.v2 = self.data['value2']

        if sum([self.v1, self.v2]) > 0:
            self._draw_regular_rect()
        else:
            self._draw_empty_rect()


def TwoValueLineChart(data, bar_color):
    if get_lang() == 'en':
        row_margin = [4, 0, 0, 0]
    elif get_lang() == 'np':
        row_margin = [6, 0, 0, 0]

    label = boil(data['label'])
    if (label == 'Ist Tranche received'):
        label = 'I<sup>st</sup> Tranche received'
    if (label == 'IInd Tranche received'):
        label = 'II<sup>nd</sup> Tranche received'
    if (label == 'IIIrd Tranche received'):
        label = 'III<sup>rd</sup> Tranche received'

    return Row(
        width='100%',
        height=16,
        margin=Rect(row_margin),
    ).add(
        Text(
            width='40%',
            markup=label,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
        ),
        # Row(width='60%', height='70%').add(add
        Row(width='60%', height='70%')
        .add(
            Canvas(
                width='100%',
                height='100%',
                renderer=Bars(data, bar_color),
            )
        )
    )


def ReconstructionStatus(data):
    rows = [
        # pass up label, v1, v2
        TwoValueLineChart(datum, bar_color=Color.ACCENT)
        for datum in data
    ]

    return Column(width='100%').add(
        Text(
            text=boil('recon_&_retrofit_reconstruction_status_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            color=Color.ACCENT,
        ),
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
        *rows,
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 1, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
    )


def Houses(data):
    return Column(width='100%').add(
        Text(
            text=boil('recon_&_retrofit_houses_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            color=Color.ACCENT,
            margin=Rect([0, 0, 2, 0])
        ),
        Row(
            width='100%',
            justify='space-between',
            margin=Rect([0, 0, 3, 0]),
        ).add(
            Text(
                markup='<b>{}</b>: {}'.format(
                    boil('recon_&_retrofit_under_construction'),
                    fmt_num(data['under_construction'],)
                ),
                font_family="Roboto Condensed",
                font_size=7.5,
            ),
            Text(
                markup='<b>{}</b>: {}'.format(
                    boil('recon_&_retrofit_completed'),
                    fmt_num(data['completed'],)
                ),
                font_family="Roboto Condensed",
                font_size=7.5,
            )
        ),
    )


def RetrofitStatus(data):
    rows = [
        TwoValueLineChart(datum, bar_color=Color.ACCENT2)
        for datum in data
    ]

    return Column(width='100%').add(
        Text(
            text=boil('recon_&_retrofit_retrofitting_status_title'),
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            color=Color.ACCENT,
        ),
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
        *rows,
        Hr(
            width='100%',
            height=1,
            margin=Rect([3, 0, 3, 0]),
            dash=[3],
            color=Color.PRIMARY,
        ),
    )


def Grievances(data):
    return Column(width='50%').add(
        Text(
            text=boil('recon_&_retrofit_grievances_title'),
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([3.2, 0, 5, 0]),
        ),
        Text(
            markup='<b>{}:</b> {}'.format(
                boil('recon_&_retrofit_registered_(both)'),
                fmt_num(data['registered']),
            ),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(
                boil('recon_&_retrofit_addressed_(both)'),
                fmt_num(data['addressed']),
            ),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def NonCompliance(data):
    return Column(width='50%').add(
        Text(
            text=boil('recon_&_retrofit_non-compliances_title'),
            color=Color.ACCENT,
            font_family="Roboto Condensed",
            font_size=9,
            font_weight=Text.BOLD,
            margin=Rect([3.2, 0, 5, 0]),
        ),
        Text(
            markup='<b>{}:</b> {}'.format(
                boil('recon_&_retrofit_registered_(both)'),
                fmt_num(data['registered']),
            ),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(
                boil('recon_&_retrofit_addressed_(both)'),
                fmt_num(data['addressed']),
            ),
            font_family="Roboto Condensed",
            font_size=7.5,
        ),
    )


def ReconstructionAndRetrofit(data):
    return Row(width='100%', padding=Rect(8)).add(
        Column(width='50%', padding=Rect([3, 8, 0, 2])).add(
            ReconstructionStatus(data['reconstruction_status']),
            Houses(data['houses']),
        ),
        Column(width='50%', padding=Rect([3, 2, 0, 8])).add(
            RetrofitStatus(data['retrofitting_status']),
            Row(width='100%').add(
                Grievances(data['grievances']),
                NonCompliance(data['non_compliances']),
            ),
        )
    )
