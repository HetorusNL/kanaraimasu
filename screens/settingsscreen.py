import pygame
from pygame.font import Font

from .screen import Screen
from utils import Collections, Settings
from widgets import Button, Checkbox, Heading, Text


class SettingsScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        self.checkboxes = {
            "randomize_kana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (600, 450, 720, 100),
                    "Randomize Kana",
                ).set_themed(),
                "setting": "randomize_kana",
            },
        }

        self.kana_widgets = {
            "hiragana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (200, 600, 700, 100),
                    "Learn Hiragana",
                ).set_themed(),
                "button": Button(
                    self.render_surface,
                    (1000, 600, 700, 100),
                    "Select which kana",
                ).set_themed(),
                "setting": "learn_hiragana",
            },
            "katakana": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (200, 750, 700, 100),
                    "Learn Katakana",
                ).set_themed(),
                "button": Button(
                    self.render_surface,
                    (1000, 750, 700, 100),
                    "Select which kana",
                ).set_themed(),
                "setting": "learn_katakana",
            },
            "kanji": {
                "checkbox": Checkbox(
                    self.render_surface,
                    (200, 900, 700, 100),
                    "Learn Kanji",
                ).set_themed(),
                "button": Button(
                    self.render_surface,
                    (1000, 900, 700, 100),
                    "Kanji options",
                ).set_themed(),
                "setting": "learn_kanji",
            },
        }

        # set the 'selected' property of the checkboxes and kana_widgets
        for checkbox_widget_id, checkbox_widget in self.checkboxes.items():
            checkbox = checkbox_widget["checkbox"]
            checkbox.selected = Settings.get(checkbox_widget["setting"])
        for kana_widget_id, kana_widget in self.kana_widgets.items():
            checkbox = kana_widget["checkbox"]
            checkbox.selected = Settings.get(kana_widget["setting"])

        theme = Settings.get("theme")
        themes = Settings.get("themes")
        self.widgets = {
            "heading_settings": Heading(
                self.render_surface, (0, 0, 1920, 100), "Settings"
            ).set_themed(),
            "button_menu": Button(
                self.render_surface, (10, 10, 230, 80), "Menu"
            ).set_themed(),
            "theme_text": Text(
                self.render_surface,
                (500, 150, 920, 100),
                f"Current theme: '{theme}'",
            ).set_themed(),
        }

        # get the theme index of the current theme
        if theme in themes:
            self.theme_index = list(themes.keys()).index(theme)
        else:
            # somehow the theme in the settings file isn't available, reset
            print(f"theme {theme} is invalid! resetting to default")
            self.theme_index = 0
            Settings.set("theme", next(iter(themes)))
            Collections.reapply_theme()

        # theme related widgets
        theme_name = list(themes.keys())[self.theme_index]
        apply_theme_text = f"Apply theme: {theme_name}"
        self.theme_left = Button(
            self.render_surface, (300, 275, 100, 100), "<"
        ).set_themed()
        self.theme_apply = Button(
            self.render_surface, (500, 275, 920, 100), apply_theme_text
        ).set_themed()
        self.theme_right = Button(
            self.render_surface, (1520, 275, 100, 100), ">"
        ).set_themed()

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
                    return {"screen_id": f"optionsfor{kana_widget_id}"}

            for checkbox_widget_id, checkbox_widget in self.checkboxes.items():
                checkbox = checkbox_widget["checkbox"]
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # checkbox is hit, save the new setting
                    Settings.set(checkbox_widget["setting"], checkbox.selected)

            # theme switcher related buttons
            if self.theme_left.rect_hit(event.pos):
                self.update_theme_index(-1)

            if self.theme_right.rect_hit(event.pos):
                self.update_theme_index(1)

            if self.theme_apply.rect_hit(event.pos):
                # get the theme from the index and save the new theme
                theme = list(Settings.get("themes").keys())[self.theme_index]
                Settings.set("theme", theme)
                # update the text on the current theme widget
                self.widgets["theme_text"].set_text(
                    f"Current theme: '{theme}'"
                )
                return {"action": "reapply_theme"}

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

        self.theme_left.render()
        self.theme_apply.render()
        self.theme_right.render()

    def update_theme_index(self, change):
        themes = Settings.get("themes")
        last_theme_index = len(themes) - 1
        # update and bounds check the theme index
        index = self.theme_index + change
        index = last_theme_index if index < 0 else index
        index = 0 if index > last_theme_index else index
        # update the class' theme index and the text
        self.theme_index = index
        apply_theme_text = f"Apply theme: {list(themes.keys())[index]}"
        self.theme_apply.set_text(apply_theme_text)
