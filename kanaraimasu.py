import pygame
from pygame.locals import RESIZABLE
import sys
import time

from utils import Settings
from screens import GameScreen, Screen

try:
    pygame.mixer.init(buffer=512)
    has_audio = True
except:
    has_audio = False
pygame.init()


class Kanaraimasu:
    def __init__(self):
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

        # initialize the screens
        self.screens = {
            "default": Screen(self.render_surface, self.render_size),
            "gamescreen": GameScreen(self.render_surface, self.render_size),
        }
        self.screen_id = "gamescreen"
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

        self.pg_screen.blit(
            pygame.transform.smoothscale(
                self.render_surface, self.screen_size
            ),
            (0, 0),
        )

        pygame.display.update()
        if self.fps != 0:
            target_sleep = 1000 / self.fps
            delta = (time.time() - self.game_time) * 1000
            if target_sleep - delta > 0:
                pygame.time.delay(int(target_sleep - delta))

    def process_event_loop(self):
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
                self.screens[self.screen_id].key_press(event)
            # handle mouse presses/releases/moves
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.screens[self.screen_id].mouse_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.screens[self.screen_id].mouse_event(event)
            elif event.type == pygame.MOUSEMOTION:
                self.screens[self.screen_id].mouse_event(event)

    def set_screen_size(self, screen_size):
        self.screen_size = screen_size
        Settings.set("width", self.screen_size[0])
        Settings.set("height", self.screen_size[1])
        for screen_id, screen in self.screens.items():
            screen.set_screen_size(self.screen_size)


if __name__ == "__main__":
    # start the main function if this script is executed
    Kanaraimasu()
