import pygame
from pygame.locals import RESIZABLE
import sys
import time

from utils import Settings, Theme
from screens import GameScreen, KanaSelectScreen, MenuScreen, SettingsScreen
from widgets import Text

try:
    pygame.mixer.init(buffer=512)
    has_audio = True
except:
    has_audio = False
pygame.init()


class Kanaraimasu:
    def __init__(self):
        # set the display name
        pygame.display.set_caption("Kanaraimasu - Learn to draw kana")

        # initialize the game parameters
        self.fps = Settings.get("fps")

        # initialize the screen and render surfaces
        width = Settings.get("width")
        height = Settings.get("height")
        fullscreen = pygame.FULLSCREEN if Settings.get("fullscreen") else 0
        self.screen_size = (width, height)
        self.pg_screen = pygame.display.set_mode(
            self.screen_size, RESIZABLE | fullscreen
        )

        self.render_size = (1920, 1080)
        self.render_surface = pygame.Surface(self.render_size)

        self.show_splash_screen()

        # initialize the screens
        self.screens = {
            "gamescreen": GameScreen(self.render_surface, self.render_size),
            "kanaselectscreenhiragana": KanaSelectScreen(
                self.render_surface, self.render_size, "hiragana"
            ),
            "kanaselectscreenkatakana": KanaSelectScreen(
                self.render_surface, self.render_size, "katakana"
            ),
            "menuscreen": MenuScreen(self.render_surface, self.render_size),
            "settingsscreen": SettingsScreen(
                self.render_surface, self.render_size
            ),
        }
        self.set_screen_id("menuscreen")
        # sets the screen size in all screens
        self.set_screen_size(self.screen_size)

        self.game_time = time.time()

        # run the game loop forever
        while True:
            self.game_loop()

    def game_loop(self):
        # process timing stuff
        current_time = time.time()
        time_delta = current_time - self.game_time
        self.game_time = current_time

        self.process_event_loop()
        self.screen_size = self.pg_screen.get_size()

        # update game logics
        self.screens[self.screen_id].update(time_delta)
        self.screens[self.screen_id].draw()

        # this draws the render_surface onto the pg_screen
        self.render()

        if self.fps != 0:
            target_sleep = 1000 / self.fps
            delta = (time.time() - self.game_time) * 1000
            if target_sleep - delta > 0:
                pygame.time.delay(int(target_sleep - delta))

    def process_event_loop(self):
        self.results = {}
        screen = self.screens[self.screen_id]
        for event in pygame.event.get():
            # handle closing the window
            if event.type == pygame.QUIT:
                print("shutting down...")
                sys.exit()
            # handle video resize events
            elif event.type == pygame.VIDEORESIZE:
                print("videoresize")
                self.set_screen_size(event.dict["size"])
            # handle minimize/maximize buttons
            elif event.type == pygame.VIDEOEXPOSE:
                print("videoexpose")
                self.set_screen_size(self.pg_screen.get_size())
            # handle key presses
            elif event.type == pygame.KEYDOWN:
                self.add_result(screen.key_press(event))
            # handle mouse presses/releases/moves
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event = self.set_render_mouse_pos(event)
                self.add_result(screen.mouse_event(event))
            elif event.type == pygame.MOUSEBUTTONUP:
                event = self.set_render_mouse_pos(event)
                self.add_result(screen.mouse_event(event))
            elif event.type == pygame.MOUSEMOTION:
                event = self.set_render_mouse_pos(event)
                self.add_result(screen.mouse_event(event))

        self.process_results()

    def set_render_mouse_pos(self, event):
        event.pos = self.s2r(event.pos)
        return event

    def add_result(self, result):
        if result:
            self.results = {**self.results, **result}

    def process_results(self):
        if self.results.get("screen_id"):
            self.set_screen_id(self.results["screen_id"])

    def set_screen_id(self, screen_id):
        self.screen_id = screen_id

        # TODO: temporary render the splash screen when gamescreen is loaded
        # till the performance issue of loading the gamescreen is fixed
        if self.screen_id == "gamescreen":
            self.show_splash_screen()

        # call prepare function so screens can do JIT (re)initialization
        # before becomming active/visible
        self.screens[self.screen_id].prepare()

    def set_screen_size(self, screen_size):
        self.screen_size = screen_size
        Settings.set("width", self.screen_size[0])
        Settings.set("height", self.screen_size[1])
        for screen_id, screen in self.screens.items():
            screen.set_screen_size(self.screen_size)

    def render(self):
        self.pg_screen.blit(
            pygame.transform.smoothscale(
                self.render_surface, self.screen_size
            ),
            (0, 0),
        )

        pygame.display.update()

    def show_splash_screen(self):
        self.render_surface.fill(Theme.get_color("background"))
        Text(
            self.render_surface, (0, 200, 1920, 400), "Kanaraimasu"
        ).set_font_size(200).set_themed().render()
        Text(
            self.render_surface, (0, 700, 1920, 200), "Loading..."
        ).set_themed().render()
        self.render()

    def s2r(self, pos):
        # convert screen coordinate/pos to render surface coordinate/pos
        x = pos[0] * self.render_size[0] / self.screen_size[0]
        y = pos[1] * self.render_size[1] / self.screen_size[1]
        return (x, y)

    def r2s(self, pos):
        # convert render surface coordinate/pos to screen coordinate/pos
        x = pos[0] * self.screen_size[0] / self.render_size[0]
        y = pos[1] * self.screen_size[1] / self.render_size[1]
        return (x, y)


if __name__ == "__main__":
    # start the main function if this script is executed
    Kanaraimasu()
