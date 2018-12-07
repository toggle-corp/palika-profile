from drafter.layouts import Row, Column
from drafter.nodes import Text
from report.common.panel import Panel
from report.common.sidebar import Sidebar
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
        text='Sources: 1. CENSUS 2011 2. NRA CBS 3. NRA 5W (25/10/2018) 4. NRA/MoFALD/MoUD (01/10/2018)',  # noqa
        font='RobotoCondensed 5',
    )


def RightFootNotes(**kwargs):
    return Text(
        **kwargs,
        text='*Note: ‘-’ indicates information not available',
        font='RobotoCondensed 5',
    )


def Page(data):
    return Column(width='100%', relative=True).add(
        Row(width='100%').add(
            Panel(
                title='Facts and Figures'.upper(),
                height=148,
                width='50% - 5',
            ).add(FF(data['facts_and_figures'])),
            Panel(
                title='Major Housing Typologies'.upper(),
                height=148,
                width='50% - 5',
            ).add(Typologies(data['housing_typologies'])),
        ),
        Row(width='100%').add(
            Panel(
                title='Housing Reconstruction & Retrofit Updates'.upper(),
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
                    title='POs PRESENCE',
                    height='45% - 20',
                    width='100% - 10',
                ).add(Pop(data['pos_presence'])),
                Panel(
                    title='OTHER SECTORS',
                    height='55% - 20',
                    width='100% - 10',
                ).add(OtherSectors(data['other_sectors'])),
            ),
            Panel(
                title='Status of construction materials'.upper(),
                width='50%',
            ).add(CMTable(data['construction_materials'], data['work_wage'])),
        ),
        Panel(
            title='Key Contacts'.upper(),
            width='100%',
            # left_footer=LeftFootNotes,
            # right_footer=RightFootNotes,
        ).add(
            KeyContacts(data['key_contacts']),
        ),
        # Sidebar(bottom=0, left=-12),
    )