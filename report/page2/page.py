from drafter.layouts import Row, Column
from report.common.panel import Panel

from .hh import HH
from .technical_staff import TechnicalStaff
from .trainings import Trainings
from .map import Map
from .footer import Footer


def Page(data):
    return Column(width='100%').add(
        Panel(
            title='HHs WITH LAND ISSUES',
            width='100% - 10',
        ).add(HH(data['hhs'])),
        Row(width='100%').add(
            Panel(
                title='Status of Technical Staff'.upper(),
                width='50% - 10',
            ).add(TechnicalStaff(data['technical_staff'])),
            Panel(
                title='Trainings'.upper(),
                height='100% - 20',
                width='50% - 10',
            ).add(Trainings(data['trainings'])),
        ),
        Panel(
            title='TA Activities Map',
            width='100% - 10',
        ).add(Map(data['map'])),
        Panel(
            title='FAQ',
            width='100% - 10',
        ).add(Footer(data['faq'])),
    )
