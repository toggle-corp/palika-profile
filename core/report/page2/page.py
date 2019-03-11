from drafter.utils import Rect
from drafter.layouts import Row, Column
from drafter.nodes import Text
from drafter.shapes import Pango

from ..common.panel import Panel
from ..common.sidebar import Sidebar
from ..common.utils import is_nan
from ..common.boiler import boil

from .hh import HH
from .technical_staff import TechnicalStaff, TechnicalStaffFooter
from .trainings import Trainings, TrainingsFooter
from .map import Map
from .footer import Footer


def FurtherInfoNotes(data, **kwargs):
    # TODO: check nans before entering

    return Row(**kwargs, width='100%', height=16).add(
        Text(
            text=boil('page_2_futher_information'),
            font_family='Roboto Condensed',
            font_size=7,
            font_weight=Pango.Weight.BOLD,
            padding=Rect([12.5, 0, 0, 5]),
        ),
        *[
            Column(width='20%', padding=Rect(8)).add(
                Text(
                    text='{}. {} ({})'.format(
                        i + 1,
                        contact['name'] if contact['name'] and contact['name'] != 'None' else '',
                        contact['title'] if contact['title'] and contact['title'] != 'None' else '',
                    ),
                    font_family='Roboto Condensed',
                    font_size=7,
                    padding=Rect([5, 0, 0, 0]),
                ),
                Text(
                    text='     {}'.format(contact['phone'] if contact['phone'] and contact['phone'] != 'None' else ''),
                    font_family='Roboto Condensed',
                    font_size=7,
                ),
            )
            for i, contact in enumerate(data)
            if not all([is_nan(v) for v in contact.values()])
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
            ).add(
                TechnicalStaff(
                    data['technical_staff'],
                    data['technical_staff_masons'],
                )
            ),
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
