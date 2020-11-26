import pygame

from .screen import Screen
from utils import Kana, Settings
from widgets import Button, Checkbox, Heading


class KanaSelectScreen(Screen):
    def __init__(self, render_surface, surface_size, kana_name):
        Screen.__init__(self, render_surface, surface_size)
        self.kana_name = kana_name
        self.kana = Kana(self.kana_name)

        self.widgets = {
            "heading_kanaselectscreen": Heading(
                self.render_surface,
                (0, 0, 1920, 100),
                f"Select Kana: {self.kana_name}",
            ),
            "button_back": Button(
                self.render_surface, (10, 10, 230, 80), "Back"
            ),
        }

        self.checkboxes = {}
        self.row_checkboxes = {}
        self.col_checkboxes = {}
        width_factor = 1520 / 6000
        height_factor = 950 / 3750
        width = 500 * width_factor
        height = 625 * height_factor

        kana_list = Settings.get(f"{self.kana_name}_kana")

        gen_checkbox = lambda kana, data: Checkbox(
            self.render_surface,
            (
                data["x"] * width_factor + 200,
                data["y"] * height_factor + 115,
                width,
                height,
            ),
            box_only=True,
        ).set_selected(kana not in kana_list)

        for kana, data in self.kana.table.items():
            self.checkboxes[kana] = gen_checkbox(kana, data)
        for row_name, data in self.kana.row_table.items():
            self.row_checkboxes[row_name] = gen_checkbox(row_name, data)
        for col_name, data in self.kana.col_table.items():
            self.col_checkboxes[col_name] = gen_checkbox(col_name, data)

        # update the rows and columns which could be wrong by default
        self._update_kana()

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

    def mouse_event(self, event):
        Screen.mouse_event(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_back"].rect_hit(event.pos):
                return {"screen_id": "settingsscreen"}

            for kana, checkbox in self.checkboxes.items():
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    self._update_kana()

            for row, checkbox in self.row_checkboxes.items():
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # find all checkboxes affected by this row
                    y = self.kana.row_table[row]["y"]
                    kana = [
                        kana
                        for kana in self.checkboxes.keys()
                        if self.kana.table[kana]["y"] == y
                    ]
                    # set the selected property the same as the row checkbox
                    for k in kana:
                        self.checkboxes[k].selected = checkbox.selected
                    # update rows and cols which could be affected
                    self._update_kana()

            for col, checkbox in self.col_checkboxes.items():
                checkbox.on_mouse_release(event.pos)
                if checkbox.rect_hit(event.pos):
                    # find all checkboxes affected by this col
                    x = self.kana.col_table[col]["x"]
                    kana = [
                        kana
                        for kana in self.checkboxes.keys()
                        if self.kana.table[kana]["x"] == x
                    ]
                    # set the selected property the same as the row checkbox
                    for k in kana:
                        self.checkboxes[k].selected = checkbox.selected
                    # update rows and cols which could be affected
                    self._update_kana()

    def draw(self):
        Screen.draw(self)
        # render widgets
        for widget_id, widget in self.widgets.items():
            widget.render()

        # draw kana table
        self.render_surface.blit(
            pygame.transform.smoothscale(self.kana.asset, (1520, 950)),
            (200, 115),
        )
        # draw the checkboxes
        for kana, checkbox in self.checkboxes.items():
            checkbox.render()
        # draw the row checkboxes
        for row, checkbox in self.row_checkboxes.items():
            checkbox.render()
        # draw the column checkboxes
        for col, checkbox in self.col_checkboxes.items():
            checkbox.render()

    def _update_kana(self):
        # update the selected status of the rows and columns
        for row, checkbox in self.row_checkboxes.items():
            y = self.kana.row_table[row]["y"]
            checkbox.selected = all(
                [
                    self.checkboxes[kana].selected
                    for kana in self.kana.characters
                    if self.kana.table[kana]["y"] == y
                ]
            )
        for col, checkbox in self.col_checkboxes.items():
            x = self.kana.col_table[col]["x"]
            checkbox.selected = all(
                [
                    self.checkboxes[kana].selected
                    for kana in self.kana.characters
                    if self.kana.table[kana]["x"] == x
                ]
            )

        # serialize the currently selected kana to settings
        selected_kana = [
            kana  # note: selected means don't learn
            for kana in self.kana.table.keys()
            if not self.checkboxes[kana].selected
        ]
        Settings.set(f"{self.kana_name}_kana", selected_kana)
