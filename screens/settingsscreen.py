import pygame
from pygame.font import Font

from .screen import Screen
from utils import Settings
from widgets import Button, Checkbox, Heading


class SettingsScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.checkboxes = {
            "dark_theme": {
                "checkbox": Checkbox(
                    self.render_surface, (600, 200, 720, 100), "Dark Theme",
                ),
                "setting": "dark_theme",
            },
            "randomize_kana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (600, 350, 720, 100),
                    "Randomize Kana",
                ),
                "setting": "randomize_kana",
            },
        }

        self.kana_widgets = {
            "hiragana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (200, 500, 700, 100),
                    "Learn Hiragana",
                ),
                "button": Button(
                    self.render_surface,
                    (1000, 500, 700, 100),
                    "Select which kana",
                ),
                "setting": "learn_hiragana",
            },
            "katakana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (200, 650, 700, 100),
                    "Learn Katakana",
                ),
                "button": Button(
                    self.render_surface,
                    (1000, 650, 700, 100),
                    "Select which kana",
                ),
                "setting": "learn_katakana",
            },
        }

        # set the 'selected' property of the checkboxes and kana_widgets
        for checkbox_widget_id, checkbox_widget in self.checkboxes.items():
            checkbox = checkbox_widget["checkbox"]
            checkbox.selected = Settings.get(checkbox_widget["setting"])
        for kana_widget_id, kana_widget in self.kana_widgets.items():
            checkbox = kana_widget["checkbox"]
            checkbox.selected = Settings.get(kana_widget["setting"])

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
            if self.widgets["button_menu"].rect_hit(event.pos):
                return {"screen_id": "menuscreen"}

            for kana_widget_id, kana_widget in self.kana_widgets.items():
                checkbox = kana_widget["checkbox"]
                # check whether the kana checkboxes are hit
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # checkbox is hit, save the new setting
                    Settings.set(kana_widget["setting"], checkbox.selected)
                # check whether the buttons are hit
                if kana_widget["button"].rect_hit(event.pos):
                    return {"screen_id": f"kanaselectscreen{kana_widget_id}"}

            for checkbox_widget_id, checkbox_widget in self.checkboxes.items():
                checkbox = checkbox_widget["checkbox"]
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # checkbox is hit, save the new setting
                    Settings.set(checkbox_widget["setting"], checkbox.selected)

    def draw(self):
        Screen.draw(self)
        for widget_id, widget in self.widgets.items():
            widget.render()

        for kana_widget_id, kana_widget in self.kana_widgets.items():
            kana_widget["checkbox"].render()
            if kana_widget["checkbox"].selected:
                kana_widget["button"].render()

        for checkbox_widget_id, checkbox_widget in self.checkboxes.items():
            checkbox_widget["checkbox"].render()
