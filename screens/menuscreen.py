import pygame
from pygame.font import Font

from .screen import Screen
from widgets import Button, Heading


class MenuScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.widgets = {
            "heading_menu": Heading(
                self.render_surface, (0, 0, 1920, 100), "Main menu"
            ),
            "button_play": Button(
                self.render_surface, (760, 450, 400, 100), "Play"
            ),
            "button_settings": Button(
                self.render_surface, (760, 600, 400, 100), "Settings"
            ),
        }

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

    def mouse_event(self, event):
        Screen.mouse_event(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_play"].rect_hit(event.pos):
                return {"screen_id": "gamescreen"}
            if self.widgets["button_settings"].rect_hit(event.pos):
                return {"screen_id": "settingsscreen"}

    def draw(self):
        Screen.draw(self)
        for widget_id, widget in self.widgets.items():
            widget.render()
