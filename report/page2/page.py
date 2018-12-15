from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text
from drafter.shapes import Pango
from report.common.panel import Panel
from report.common.sidebar import Sidebar

from .hh import HH
from .technical_staff import TechnicalStaff, TechnicalStaffFooter
from .trainings import Trainings, TrainingsFooter
from .map import Map
from .footer import Footer
from report.common.boiler import boil


def FurtherInfoNotes(data, **kwargs):
    return Row(**kwargs, width='100%', height=16).add(
        Text(
            text=boil('page_2_futher_information'),
            font_family='Roboto Condensed',
            font_size=5.5,
            font_weight=Pango.Weight.BOLD,
            padding=Rect([8, 0, 8, 0]),
        ),
        *[
            Column(width='30%', padding=Rect(8)).add(
                Text(
                    text='{}. {} ({})'.format(
                        i + 1,
                        contact['name'],
                        contact['title'],
                    ),
                    font_family='Roboto Condensed',
                    font_size=5.5,
                ),
                Text(
                    text='     {}'.format(contact['phone']),
                    font_family='Roboto Condensed',
                    font_size=5.5,
                ),
            )
            for i, contact in enumerate(data)
        ]
    )


def Page(data):
    return Column(width='100%', relative=True).add(
        Panel(
            title=boil('land_issues_panel_title'),
            width='100% - 10',
        ).add(HH(data['hhs'])),
        Row(width='100%').add(
            Panel(
                title=boil('tech_staff_panel_title'),
                width='50% - 10',
                right_footer=TechnicalStaffFooter,
            ).add(TechnicalStaff(data['technical_staff'], data['technical_staff_masons'])),
            Panel(
                title=boil('training_panel_title'),
                height='100% - 20',
                width='50% - 10',
                right_footer=TrainingsFooter,
            ).add(Trainings(data['trainings'])),
        ),
        Panel(
            title=boil('map_panel_title'),
            width='100% - 10',
        ).add(Map(data['map'])),
        Panel(
            title=boil('faq_panel_title'),
            width='100% - 10',
            left_footer=FurtherInfoNotes,
            footer_data=data['further_info'],
        ).add(Footer(data['faq'])),
        Sidebar(bottom=0, right=-12),
    )
