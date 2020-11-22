import pygame
from pygame.font import Font

from .screen import Screen
from widgets import Button, Heading


class SettingsScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.widgets = {
            "heading_settings": Heading(
                self.render_surface, (0, 0, 1920, 100), "Settings"
            ),
            "button_menu": Button(
                self.render_surface, (10, 10, 230, 80), "Menu"
            ),
        }

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

    def mouse_event(self, event):
        Screen.mouse_event(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_menu"].rect_hit(self.s2r(event.pos)):
                return {"screen_id": "menuscreen"}

    def draw(self):
        Screen.draw(self)
        for widget_id, widget in self.widgets.items():
            widget.render()
