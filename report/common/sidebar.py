from drafter.utils import Rect
from drafter.layouts import Row
from drafter.nodes import Text, Image


def Label(text):
    return Text(
        text=text,
        font='RobotoCondensed 6',
        padding=Rect(2),
    )


def Icon(filename):
    return Image(
        filename='resources/images/{}'.format(filename),
        width=18,
        height=16,
        padding=Rect([2, 2, 2, 4]),
    )


def Sidebar(**kwargs):
    children = [
        Label('Connect with us:'.upper()),
        Icon('fb.png'),
        Label('HRRPNepal'),
        Icon('twitter.png'),
        Label('HRRP_Nepal'),
        Icon('flipboard.png'),
        Label('/photos/hrrp'),
        Icon('flickr.png'),
        Label('@HRRP'),
    ]

    return Row(
        absolute=True,
        height=16,
        width=16,
        angle=-90,
        align='end',
        **kwargs,
    ).add(*children)
