from drafter.layouts import Row, Column
from drafter.nodes import Text

from report.common.panel import Panel
from report.common.sidebar import Sidebar
from report.common.boiler import boil
from .ff import FF
from .reconstruction import ReconstructionAndRetrofit
from .cm_table import CMTable
from .pop import Pop
from .typologies import Typologies
from .other_sectors import OtherSectors
from .key_contacts import KeyContacts



def LeftFootNotes(**kwargs):
    return Text(
        **kwargs,
        text=boil('page_1_sources_footer'),
        font='RobotoCondensed 5',
    )


def RightFootNotes(**kwargs):
    return Text(
        **kwargs,
        text=boil('page_1_no_info_footer'),
        font='RobotoCondensed 5',
    )


def Page(data):
    return Column(width='100%', relative=True).add(
        Row(width='100%').add(
            Panel(
                title=boil('facts_and_figures_panel_title'),
                height=148,
                width='50% - 5',
            ).add(FF(data['facts_and_figures'])),
            Panel(
                title=boil('typologies_panel_title'),
                height=148,
                width='50% - 5',
            ).add(Typologies(data['housing_typologies'])),
        ),
        Row(width='100%').add(
            Panel(
                title=boil('recon_&_retrofit_panel_title'),
                width='100%',
            ).add(
                ReconstructionAndRetrofit(
                    data['reconstruction_retrofit_updates']
                ),
            ),
        ),
        Row(width='100%').add(
            Column(width='50%', height='100%').add(
                Panel(
                    title=boil('po_presence_pos_presence_title'),
                    height='45% - 20',
                    width='100% - 10',
                ).add(Pop(data['pos_presence'])),
                Panel(
                    title=boil('other_sectors_panel_title'),
                    height='55% - 20',
                    width='100% - 10',
                ).add(OtherSectors(data['other_sectors'])),
            ),
            Panel(
                title=boil('status_of_cm_panel_title'),
                width='50%',
            ).add(CMTable(data['construction_materials'], data['work_wage'])),
        ),
        Panel(
            title=boil('key_contacts_panel_title'),
            width='100%',
            left_footer=LeftFootNotes,
            right_footer=RightFootNotes,
        ).add(
            KeyContacts(data['key_contacts']),
        ),
        Sidebar(bottom=0, left=-12),
    )