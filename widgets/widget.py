import pygame
from pygame.font import Font


class Widget:
    def __init__(self, surface, rect):
        self.surface = surface
        self.rect = pygame.Rect(rect)

    # setters for the properties, they return self so are chainable
    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)
        return self

    # basic functions for the widget
    def on_mouse_release(self, pos):
        # this function calls on_click if a mouse release event happens
        # within this button's rectangle
        if self.rect_hit(pos):
            self.on_click(pos)

    def on_click(self, pos):
        # this function can be overridden where used,
        # by using a function or a lambda function
        pass

    def render(self):
        pass

    def rect_hit(self, pos):
        # returns true if the given point is inside the rectangle. a point
        # along the right/bottom edge is not considered to be inside the rect
        return self.rect.collidepoint(pos)
