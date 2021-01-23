import pygame
from pygame.font import Font
import random

from .screen import Screen
from utils import Kana, Settings, Theme
from widgets import Button, Heading, Text


class GameScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        # the surface where the user draws on
        self.drawing_surface = pygame.Surface(self.surface_size)

        self.stroke_width = Settings.get("stroke_width")
        self.bounding_box_color = Theme.get_color("foreground")
        self.cross_color = Theme.get_color("secondary")
        self.draw_color = Theme.get_color("draw")

        # ingame parameters
        self.pos = (0, 0)

        # widgets that are always present
        self.widgets = {
            "heading": Heading(
                self.render_surface, (0, 0, 1920, 100)
            ).set_themed(),
            "button_menu": Button(
                self.render_surface, (10, 10, 230, 80), "Menu"
            ).set_themed(),
        }

        # widgets in draw state
        self.clear_button = (
            Button(self.render_surface, (860, 290, 200, 150), "Clear")
            .set_font_size(90)
            .set_themed()
        )
        self.done_button = Button(
            self.render_surface, (860, 490, 200, 200), "Done"
        ).set_themed()

        # widgets in the verify state
        self.wrong_button = (
            Button(self.render_surface, (860, 290, 200, 150), "Wrong")
            .set_font_size(80)
            .set_themed()
            .set_rect_color(Theme.get_color("bad"))
        )
        self.good_button = (
            Button(self.render_surface, (860, 490, 200, 200), "Good")
            .set_themed()
            .set_rect_color(Theme.get_color("good"))
        )

        # widgets in the done state
        self.score_widget = Text(
            self.render_surface,
            (0, 550, 1920, 200),
            "Learned x kana while making y mistakes",
        ).set_themed()
        done_widgets = [
            Text(self.render_surface, (0, 400, 1920, 200), "Done!")
            .set_font_size(200)
            .set_themed(),
            self.score_widget,
            Text(
                self.render_surface,
                (0, 650, 1920, 200),
                "Go back to the menu to try again,",
            ).set_themed(),
            Text(
                self.render_surface,
                (0, 750, 1920, 200),
                "or change the kana you want to learn",
            ).set_themed(),
        ]

        self.state_widgets = {
            "draw": [self.clear_button, self.done_button],
            "verify": [self.wrong_button, self.good_button],
            "done": done_widgets,
        }

    def prepare(self):
        self.randomize_kana = Settings.get("randomize_kana")
        # load the selected kana from the hiragana/katakana tables
        self.selected_kana = []
        kana_names = ["hiragana", "katakana"]
        for kana_name in kana_names:
            kana = Kana(kana_name)
            if not Settings.get(f"learn_{kana_name}"):
                continue
            for kana_name in Settings.get(f"{kana_name}_kana"):
                self.selected_kana.append({"kana": kana, "name": kana_name})

        # parameters for the scoring system
        self.total_kana = len(self.selected_kana)
        self.wrong_kana = 0

        # handle case where no kana is selected
        if not self.selected_kana:
            self._update_scoring_system()
            self.state = "done"
            self._clear_drawing_surface()
            return

        # start with some initial index
        if self.randomize_kana:
            # if randomize, simply get a random index from the kana left
            self.index = random.randint(0, len(self.selected_kana) - 1)
        else:
            # if not randomized, start at the first kana, index 0
            self.index = 0

        # get a reference to the current kana
        self.kana = self.selected_kana[self.index]

        self.state = "draw"
        self._clear_drawing_surface()

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

    def _draw_done(self):
        self.state = "verify"

    def _verify_done(self, correct):
        self.state = "draw"
        self._clear_drawing_surface()

        # handle correctly drawn kana
        if correct:
            del self.selected_kana[self.index]
            if len(self.selected_kana) == 0:
                self._update_scoring_system()
                self.state = "done"
                return
        else:
            self.wrong_kana += 1

        if self.randomize_kana:
            # if randomize, simply get a random index from the kana left
            self.index = random.randint(0, len(self.selected_kana) - 1)
        else:
            # if not randomized, increment index on correct
            if not correct:
                self.index += 1
            # handle overflow of index
            if self.index >= len(self.selected_kana):
                self.index = 0

        # get a reference to the current kana
        self.kana = self.selected_kana[self.index]

    def _update_scoring_system(self):
        self.score_widget.set_text(
            f"Learned {self.total_kana} kana "
            f"while making {self.wrong_kana} mistakes"
        )

    def mouse_event(self, event):
        Screen.mouse_event(self, event)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_menu"].rect_hit(event.pos):
                return {"screen_id": "menuscreen"}

        # if we're inside the Done rect, don't perform the drawing
        if self.state == "draw":
            if self.clear_button.rect_hit(event.pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._clear_drawing_surface()
                return
            if self.done_button.rect_hit(event.pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._draw_done()
                return
        if self.state == "verify":
            if self.wrong_button.rect_hit(event.pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._verify_done(False)
                return
            if self.good_button.rect_hit(event.pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._verify_done(True)
                return

        # update the line drawing
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            self._draw_line(self.pos, event.pos)
        self.pos = event.pos

    def _clamp_pos(self, pos):
        x = max(pos[0], 100 + self.stroke_width)
        x = min(x, 760 - self.stroke_width)
        y = max(pos[1], 260 + self.stroke_width)
        y = min(y, 920 - self.stroke_width)
        return (x, y)

    def _draw_line(self, pos1, pos2):
        return self._draw_polygon(self._clamp_pos(pos1), self._clamp_pos(pos2))

    def _draw_polygon(self, pos1, pos2):
        # TODO: refactor this into drawing 2 tangent closing lines between
        # the circles
        a = [
            (pos1[0] + self.stroke_width // 2, pos1[1]),
            (pos2[0] + self.stroke_width // 2, pos2[1]),
            (pos2[0] - self.stroke_width // 2, pos2[1]),
            (pos1[0] - self.stroke_width // 2, pos1[1]),
        ]
        b = [
            (pos1[0], pos1[1] + self.stroke_width // 2),
            (pos2[0], pos2[1] + self.stroke_width // 2),
            (pos2[0], pos2[1] - self.stroke_width // 2),
            (pos1[0], pos1[1] - self.stroke_width // 2),
        ]
        pygame.draw.polygon(self.drawing_surface, self.draw_color, a)
        pygame.draw.polygon(self.drawing_surface, self.draw_color, b)

        self._pg_draw_circle(pos1, self.stroke_width // 2, self.draw_color)
        self._pg_draw_circle(pos2, self.stroke_width // 2, self.draw_color)

    def _clear_drawing_surface(self):
        self.drawing_surface.fill((255, 255, 255, 0))
        self.drawing_surface = self.drawing_surface.convert_alpha()
        self.drawing_surface.fill((0, 0, 0, 0))

    def draw(self):
        Screen.draw(self)

        if self.state == "draw":
            # add message to user to draw character
            self.widgets["heading"].set_text(
                f'Draw the {self.kana["kana"].table_name} '
                f'character for {self.kana["name"].upper()}'
            )
        elif self.state == "verify":
            # add message to user to verify character
            self.widgets["heading"].set_text(
                f'Verify the {self.kana["kana"].table_name} '
                f'character for {self.kana["name"].upper()}'
            )
            # draw character here
            character = self.kana["kana"].table[self.kana["name"]]
            if all(color < 50 for color in self.background_color):
                kana = self.kana["kana"]
                pygame.draw.rect(
                    self.render_surface,
                    (50, 50, 50),
                    (1260, 260, kana.size_x, kana.size_y),
                )
            self.render_surface.blit(
                self.kana["kana"].asset,
                (1260, 260),
                character["rect"],
            )
        elif self.state == "done":
            self.widgets["heading"].set_text("All kana drawn successfully")

        # render the widgets
        for widget_id, widget in self.widgets.items():
            widget.render()
        # render the state widgets
        for widget in self.state_widgets[self.state]:
            widget.render()

        if self.state == "done":
            # if we're done don't draw the drawing surface
            return

        # always draw a bounding box where the user should draw in
        self._pg_draw_line((430, 260), (430, 920), 10, self.cross_color)
        self._pg_draw_line((100, 590), (760, 590), 10, self.cross_color)
        self._pg_draw_rect((100, 260, 660, 660), 10, self.bounding_box_color)

        # also always render the drawing surface
        self.render_surface.blit(self.drawing_surface, (0, 0))

    def _pg_draw_line(self, top_left, bot_right, width, color=None):
        color = color or self.foreground_color
        pygame.draw.line(
            self.render_surface, color, top_left, bot_right, width
        )

    def _pg_draw_rect(self, rect, width, color=None):
        color = color or self.foreground_color
        pygame.draw.rect(self.render_surface, color, rect, width)

    def _pg_draw_circle(self, center, radius, color=None):
        color = color or self.foreground_color
        pygame.draw.circle(self.drawing_surface, color, center, radius)

    def reapply_theme(self, foreground_color, background_color):
        Screen.reapply_theme(self, foreground_color, background_color)
        self.wrong_button.set_rect_color(Theme.get_color("bad"))
        self.good_button.set_rect_color(Theme.get_color("good"))
        self.bounding_box_color = Theme.get_color("foreground")
        self.cross_color = Theme.get_color("secondary")
        self.draw_color = Theme.get_color("draw")
