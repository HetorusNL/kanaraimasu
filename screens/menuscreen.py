import pygame

from .screen import Screen
from widgets import Button, Heading


class MenuScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.widgets = {
            "heading_menu": Heading(
                self.render_surface, (0, 0, 1920, 100), "Main menu"
            ).set_themed(),
            "button_play": Button(
                self.render_surface, (760, 450, 400, 100), "Play"
            ).set_themed(),
            "button_settings": Button(
                self.render_surface, (760, 600, 400, 100), "Settings"
            ).set_themed(),
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
