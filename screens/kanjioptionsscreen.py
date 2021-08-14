import pygame

from .screen import Screen
from utils import Settings
from widgets import Button, Checkbox, Heading


class KanjiOptionsScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.widgets = {
            "heading_kanjioptionsscreen": Heading(
                self.render_surface, (0, 0, 1920, 100), "Kanji Options"
            ).set_themed(),
            "button_back": Button(
                self.render_surface, (10, 10, 230, 80), "Back"
            ).set_themed(),
        }

        self.checkboxes = {
            "kanji_show_kun": Checkbox(
                self.render_surface, (600, 400, 720, 100), "Show 'kun' reading"
            ).set_themed(),
            "kanji_show_on": Checkbox(
                self.render_surface, (600, 550, 720, 100), "Show 'on' reading"
            ).set_themed(),
            "kanji_show_dutch": Checkbox(
                self.render_surface, (600, 700, 720, 100), "Show Dutch"
            ).set_themed(),
        }

        # set the 'selected' property of the checkboxes
        for checkbox_id, checkbox in self.checkboxes.items():
            checkbox.selected = Settings.get(checkbox_id)

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

    def mouse_event(self, event):
        Screen.mouse_event(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_back"].rect_hit(event.pos):
                return {"screen_id": "settingsscreen"}

            for checkbox_id, checkbox in self.checkboxes.items():
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # checkbox is hit, save the new setting
                    Settings.set(checkbox_id, checkbox.selected)

    def draw(self):
        Screen.draw(self)
        # render widgets
        for widget_id, widget in self.widgets.items():
            widget.render()
        # render checkboxes
        for checkbox_id, checkbox in self.checkboxes.items():
            checkbox.render()

    def reapply_theme(self):
        Screen.reapply_theme(self)