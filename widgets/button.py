import pygame

from .text import Text
from utils import Theme


class Button(Text):
    def __init__(
        self,
        surface,
        rect,
        text="",
        color=None,
        width=10,
        align=Text.ALIGN_CENTER,
    ):
        Text.__init__(self, surface, rect, text, color, width, align)
        color = color or Theme.get_color()
        self.rect_color = color

    # setters for the properties, they return self so are chainable
    def set_color(self, color):
        Text.set_color(self, color)
        self.set_rect_color(color)
        return self

    def set_rect_color(self, color):
        self.rect_color = color
        return self

    # basic functions for the widget
    def render(self):
        # draw the Text widget
        Text.render(self)
        # draw the rectangle
        pygame.draw.rect(self.surface, self.rect_color, self.rect, self.width)
