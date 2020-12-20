import pygame

from .text import Text
from utils import Theme


class Checkbox(Text):
    def __init__(
        self,
        surface,
        rect,
        text="",
        color=None,
        width=10,
        align=Text.ALIGN_CENTER,
        box_only=False,
        bounding_box=False,
    ):
        self.full_rect = pygame.Rect(rect)
        if box_only:
            # render only a box over the full rect provided
            self.square_rect = self.full_rect
            Text.__init__(self, surface, rect, text, color, width)
        else:
            # render a square box and the text behind that
            r = pygame.Rect(rect)
            # create rect for the checkbox itself
            self.square_rect = pygame.Rect(r.x, r.y, r.h, r.h)
            # subtract the square checkbox (and 25%) from the text rect
            rect = (r.x + r.h + r.h * 0.25, r.y, r.w - r.h, r.h)
            Text.__init__(
                self, surface, rect, text, color, width, Text.ALIGN_LEFT_CENTER
            )

        # the two lines that make a cross in the checkbox
        sr = self.square_rect  # use small variable name here
        self.cross = [
            ((sr.x, sr.y), (sr.x + sr.w, sr.y + sr.h)),
            ((sr.x + sr.w, sr.y), (sr.x, sr.y + sr.h)),
        ]
        color = color or Theme.get_color()
        self.rect_color = color
        self.bounding_box = bounding_box
        self.selected = False

    # setters for the properties, they return self so are chainable
    def set_color(self, color):
        Text.set_color(self, color)
        self.set_rect_color(color)
        return self

    def set_rect_color(self, color):
        self.rect_color = color
        return self

    def set_selected(self, selected):
        self.selected = selected
        return self

    # basic functions for the widget
    # override rect_hit to check the whole rect
    def rect_hit(self, pos):
        # returns true if the given point is inside the rectangle. a point
        # along the right/bottom edge is not considered to be inside the rect
        return self.full_rect.collidepoint(pos)

    # override on_click so that the 'selected' property gets inverted
    def on_click(self, pos):
        Text.on_click(self, pos)
        self.selected = not self.selected

    def render(self):
        # draw the Text widget (only when there is text to render)
        if self.text:
            Text.render(self)
        # draw the checkbox itself
        pygame.draw.rect(
            self.surface, self.rect_color, self.square_rect, self.width
        )
        # draw a cross if the checkbox is selected
        if self.selected:
            for line in self.cross:
                pygame.draw.line(
                    self.surface, self.rect_color, line[0], line[1], self.width
                )
        # if bounding box is selected (debug) draw a bounding box
        if self.bounding_box:
            pygame.draw.rect(
                self.surface, self.rect_color, self.full_rect, self.width
            )
