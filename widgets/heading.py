import pygame

from .text import Text
from utils import Theme


class Heading(Text):
    def __init__(
        self,
        surface,
        rect,
        text="",
        color=None,
        themed=None,
        width=10,
        align=Text.ALIGN_CENTER,
    ):
        Text.__init__(self, surface, rect, text, color, themed, width, align)
        color = Theme.get_color() if (themed or color is None) else color
        self.line_color = color

    # setters for the properties, they return self so are chainable
    def set_color(self, color):
        Text.set_color(self, color)
        self.set_line_color(color)
        return self

    def set_line_color(self, color):
        self.line_color = color
        return self

    # basic functions for the widget
    def render(self):
        # draw the Text widget
        Text.render(self)
        # draw the line
        pygame.draw.line(
            self.surface,
            self.line_color,
            self.rect.bottomleft,
            self.rect.bottomright,
            self.width,
        )
