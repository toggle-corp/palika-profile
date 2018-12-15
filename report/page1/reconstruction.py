from drafter.utils import Rect
from drafter.shapes import Shape, Rectangle, String
from drafter.layouts import Row, Column
from drafter.nodes import Text, Hr, Canvas
from drafter.shapes import Pango

from report.common.color import Color
from report.common.utils import fmt_num, get_text_width
from report.common.boiler import boil


class Bars(Shape):
    def __init__(self, data):
        self.data = data

    def x_pos_v1(self):
        if (self.v1_len + self.NUM_PAD) > self.r1_w:
            self.inv_v1_col = True
            return self.r1_w + self.NUM_PAD
        else:
            return self.NUM_PAD

    def x_pos_v2(self):
        if (self.v2_len + self.NUM_PAD) > self.r2_w:
            self.inv_v2_col = True
            return self.r1_w - self.v2_len - 2
        else:
            return self.F_W - self.v2_len - 2

    def render(self, ctx):
        self.F_W = 148
        self.NUM_PAD = 2
        font_family = 'Roboto'
        font_size = 8
        font_weight = Pango.Weight.BOLD
        color = Color.WHITE

        v1 = self.data['value1']
        v2 = self.data['value2']

        self.v1_str = fmt_num(v1)
        self.v2_str = fmt_num(v2)

        if self.v1_str == '0':
            self.v1_str = ''
        if self.v2_str == '0':
            self.v2_str = ''

        self.inv_v1_col = False
        self.inv_v2_col = False

        self.v1_len = get_text_width(self.v1_str, font_size, font_family, 'bold')
        self.v2_len = get_text_width(self.v2_str, font_size, font_family, 'bold')

        self.r1_w = (v1 / (v1 + v2)) * self.F_W
        self.r2_w = (v2 / (v1 + v2)) * self.F_W

        #v1 rect
        Rectangle(
            pos=[0, 0],
            size=[self.r1_w, 12],
            color=Color.ORANGE,
            line_width=0,
        ).render(ctx),

        #v2 rect
        Rectangle(
            pos=[self.r1_w, 0],
            size=[self.F_W - self.r1_w, 12],
            color=Color.GRAY,
            line_width=0,
        ).render(ctx)

        #v1 string
        String(
            pos=[self.x_pos_v1(), 1],
            markup=self.v1_str,
            font_family=font_family,
            font_size=font_size,
            font_weight=font_weight,
            color=Color.WHITE if not self.inv_v1_col else Color.ORANGE,
            alignment=String.LEFT,
        ).render(ctx)

        #v2 string
        String(
            pos=[self.x_pos_v2(), 1.5],
            markup=self.v2_str,
            font_family=font_family,
            font_size=font_size,
            font_weight=font_weight,
            color=Color.WHITE if not self.inv_v2_col else Color.GRAY,
            alignment=String.LEFT,
        ).render(ctx)

def TwoValueLineChart(data, color):

    return Row(
        width='100%',
        height=16,
        margin=Rect([4, 0, 0, 0]),
    ).add(
        Text(
            width='40%',
            text=boil(data['label']),
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
                    renderer=Bars(data),
                )
        )
    )

def ReconstructionStatus(data):
    rows = [
        #pass up label, v1, v2
        TwoValueLineChart(datum, color=Color.ACCENT)
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
                markup='<b>{}</b>: {}'.format(boil('recon_&_retrofit_under_construction'),
                                              fmt_num(data['under_construction'])
                                              ),
                font_family="Roboto Condensed",
                font_size=7.5,
            ),
            Text(
                markup='<b>{}</b>: {}'.format(boil('recon_&_retrofit_completed'),
                                              fmt_num(data['completed'])
                                              ),
                font_family="Roboto Condensed",
                font_size=7.5,
            )
        ),
    )


def RetrofitStatus(data):
    rows = [
        TwoValueLineChart(datum, color=Color.ACCENT2)
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
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_registered_(both)'), fmt_num(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_addressed_(both)'), fmt_num(data['addressed'])),
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
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_registered_(both)'), fmt_num(data['registered'])),
            font_family="Roboto Condensed",
            font_size=7.5,
            margin=Rect([0, 0, 3, 0])
        ),
        Text(
            markup='<b>{}:</b> {}'.format(boil('recon_&_retrofit_addressed_(both)'), fmt_num(data['addressed'])),
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
