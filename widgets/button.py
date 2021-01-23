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
        themed=None,
        width=10,
        align=Text.ALIGN_CENTER,
    ):
        Text.__init__(self, surface, rect, text, color, themed, width, align)
        if themed or color is None:
            # draw a filled rectangle with primary color
            self.rect_color = Theme.get_color("primary")
        else:
            # draw a border around the button with foreground color
            self.rect_color = Theme.get_color("foreground")

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
        if self.themed:
            # draw the filled rectangle
            pygame.draw.rect(self.surface, self.rect_color, self.rect, 0)
        else:
            # draw the border around the button
            pygame.draw.rect(
                self.surface, self.rect_color, self.rect, self.width
            )
        # draw the Text widget (on top of the rectangle)
        Text.render(self)

    def reapply_theme(self):
        if self.themed:
            Text.set_color(self, Theme.get_color())
            self.set_rect_color(Theme.get_color("primary"))
