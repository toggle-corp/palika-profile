from drafter.layouts import Row, Column
from report.common.panel import Panel
from .ff import FF
from .reconstruction import ReconstructionAndRetrofit
from .cm_table import CMTable
from .pop import Pop
from .typologies import Typologies
from .other_sectors import OtherSectors
from .key_contacts import KeyContacts


def Page():
    return Column(width='100%').add(
        Row(width='100%').add(
            Panel(
                title='Facts and Figures'.upper(),
                height=148,
                width='50% - 5',
            ).add(FF()),
            Panel(
                title='Major Housing Typologies'.upper(),
                height=148,
                width='50% - 5',
            ).add(Typologies()),
        ),
        Row(width='100%').add(
            Panel(
                title='Housing Reconstruction & Retrofit Updates'.upper(),
                width='100%',
            ).add(
                ReconstructionAndRetrofit(),
            ),
        ),
        Row(width='100%').add(
            Column(width='50%', height='100%').add(
                Panel(
                    title='POs PRESENCE',
                    height='40% - 20',
                    width='100% - 10',
                ).add(Pop()),
                Panel(
                    title='OTHER SECTORS',
                    height='60% - 20',
                    width='100% - 10',
                ).add(OtherSectors()),
            ),
            Panel(
                title='Status of construction materials'.upper(),
                width='50%',
            ).add(CMTable()),
        ),
        Panel(
            title='Key Contacts'.upper(),
            width='100%',
        ).add(
            KeyContacts(),
        )
    )
