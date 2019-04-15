from drafter.utils import Rect
from drafter.layouts import Row
from drafter.nodes import Text, Image

from ..common.boiler import boil
from ..common.utils import get_resource_abspath


def Label(text):
    return Text(
        text=text,
        font='RobotoCondensed',
        font_size=6,
        padding=Rect(2),
    )


def Icon(filename):
    return Image(
        filename=get_resource_abspath('images/{}'.format(filename)),
        width=18,
        height=16,
        padding=Rect([2, 2, 2, 4]),
    )


def Sidebar(**kwargs):
    children = [
        Label(boil('social_connect')),
        Icon('hrrp.png'),
        Label('www.hrrpnepal.org'),
        Icon('fb.png'),
        Label(boil('social_fb')),
        Icon('twitter.png'),
        Label(boil('social_twitter')),
        Icon('flipboard.png'),
        Label(boil('social_pinterest?')),
        Icon('flickr.png'),
        Label(boil('social_flickr')),
    ]

    return Row(
        absolute=True,
        height=16,
        width=16,
        angle=-90,
        align='end',
        **kwargs,
    ).add(*children)
