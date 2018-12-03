from drafter.color import rgb, rgba, hx


class Color:
    BLACK = rgb(0, 0, 0)
    WHITE = rgb(255, 255, 255)
    GRAY = rgba(0, 0, 0, 0.2)

    BLUE = rgb(26, 35, 126)

    ORANGE = hx('#ed7d31')
    DARK_ORANGE = hx('e76726')

    GREEN = hx('#00b050')
    DARK_GREEN = hx('#278a4f')

    PRIMARY = BLUE
    ACCENT = ORANGE
    ACCENT2 = GREEN
