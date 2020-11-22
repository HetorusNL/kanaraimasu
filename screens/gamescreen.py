import pygame
from pygame.font import Font

from .screen import Screen
from utils import Kana, Settings
from widgets import Button, Heading


class GameScreen(Screen):
    def __init__(self, render_surface, surface_size):
        Screen.__init__(self, render_surface, surface_size)

        # the surface where the user draws on
        self.drawing_surface = pygame.Surface(self.surface_size)
        self._clear_drawing_surface()

        self.kana = Kana("hiragana")
        self.value = 0
        self.index = 0

        self.stroke_width = Settings.get("stroke_width")

        # ingame parameters
        self.fonts = {"100": Font(None, 100)}
        self.pos = (0, 0)
        self.state = "draw"

        # widgets that are always present
        self.widgets = {
            "heading": Heading(self.render_surface, (0, 0, 1920, 100)),
            "button_menu": Button(
                self.render_surface, (10, 10, 230, 80), "Menu"
            ),
        }

        # widgets in draw state
        self.clear_button = Button(
            self.render_surface, (860, 290, 200, 150), "Clear"
        ).set_font_size(90)
        self.done_button = Button(
            self.render_surface, (860, 490, 200, 200), "Done"
        )

        # widgets in the verify state
        self.wrong_button = Button(
            self.render_surface, (860, 290, 200, 150), "Wrong", (100, 0, 0)
        ).set_font_size(80)
        self.good_button = Button(
            self.render_surface, (860, 490, 200, 200), "Good", (0, 100, 0)
        )

        self.state_widgets = {
            "draw": [self.clear_button, self.done_button],
            "verify": [self.wrong_button, self.good_button],
        }

    def update(self, delta_time):
        Screen.update(self, delta_time)

    def key_press(self, event):
        Screen.key_press(self, event)

        if self.state == "draw":
            self._draw_done()
        elif self.state == "verify":
            self._verify_done()

    def _draw_done(self):
        self.state = "verify"

    def _verify_done(self):
        self.state = "draw"
        self._clear_drawing_surface()

        self.index += 1
        if self.index >= len(self.kana.table):
            self.index = 0

    def mouse_event(self, event):
        Screen.mouse_event(self, event)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.widgets["button_menu"].rect_hit(self.s2r(event.pos)):
                return {"screen_id": "menuscreen"}

        # if we're inside the Done rect, don't perform the drawing
        if self.state == "draw":
            if self.clear_button.rect_hit(self.s2r(event.pos)):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._clear_drawing_surface()
                return
            if self.done_button.rect_hit(self.s2r(event.pos)):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._draw_done()
                return
        if self.state == "verify":
            if self.wrong_button.rect_hit(self.s2r(event.pos)):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._verify_done()
                return
            if self.good_button.rect_hit(self.s2r(event.pos)):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._verify_done()
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
        p1 = self.s2r(pos1)
        p2 = self.s2r(pos2)
        return self._draw_polygon(self._clamp_pos(p1), self._clamp_pos(p2))

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
        pygame.draw.polygon(self.drawing_surface, (0, 0, 255), a)
        pygame.draw.polygon(self.drawing_surface, (0, 0, 255), b)

        self._pg_draw_circle(pos1, self.stroke_width // 2, (0, 0, 255))
        self._pg_draw_circle(pos2, self.stroke_width // 2, (0, 0, 255))

    def _clear_drawing_surface(self):
        self.drawing_surface.fill((255, 255, 255, 0))
        self.drawing_surface = self.drawing_surface.convert_alpha()
        self.drawing_surface.fill((0, 0, 0, 0))

    def draw(self):
        Screen.draw(self)

        # always draw a bounding box where the user should draw in
        self._pg_draw_line((430, 260), (430, 920), 10, (200, 200, 200))
        self._pg_draw_line((100, 590), (760, 590), 10, (200, 200, 200))
        self._pg_draw_rect((100, 260, 660, 660), 10)

        # also always render the drawing surface
        self.render_surface.blit(self.drawing_surface, (0, 0))

        if self.state == "draw":
            # add message to user to draw character
            self.widgets["heading"].set_text(
                f"Draw the {self.kana.table_name} character "
                f"for {self.kana.characters[self.index].upper()}"
            )
        elif self.state == "verify":
            # add message to user to verify character
            self.widgets["heading"].set_text(
                f"Verify the {self.kana.table_name} character "
                f"for {self.kana.characters[self.index].upper()}"
            )
            # draw character here
            character = self.kana.table[self.kana.characters[self.index]]
            self.render_surface.blit(
                self.kana.asset, (1260, 260), character["rect"],
            )

        # render the widgets
        for widget_id, widget in self.widgets.items():
            widget.render()
        # render the state widgets
        for widget in self.state_widgets[self.state]:
            widget.render()

    def _pg_draw_line(self, top_left, bot_right, width, color=(0, 0, 0)):
        pygame.draw.line(
            self.render_surface, color, top_left, bot_right, width
        )

    def _pg_draw_rect(self, rect, width, color=(0, 0, 0)):
        pygame.draw.rect(self.render_surface, color, rect, width)

    def _pg_draw_circle(self, center, radius, color=(0, 0, 0)):
        pygame.draw.circle(self.drawing_surface, color, center, radius)
