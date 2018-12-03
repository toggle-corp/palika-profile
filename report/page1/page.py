from drafter.layouts import Row, Column
from report.common.panel import Panel
from .ff import FF
from .reconstruction import ReconstructionAndRetrofit
from .cm_table import CMTable
from .pop import Pop
from .typologies import Typologies
from .other_sectors import OtherSectors
from .key_contacts import KeyContacts


def Page(data):
    return Column(width='100%').add(
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
            ).add(CMTable(data['construction_materials'])),
        ),
        Panel(
            title='Key Contacts'.upper(),
            width='100%',
        ).add(
            KeyContacts(data['key_contacts']),
        )
    )
