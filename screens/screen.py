from utils import Collections, Theme


class Screen:
    def __init__(self, render_surface, surface_size):
        self.render_surface = render_surface
        self.surface_size = surface_size
        self.foreground_color = Theme.get_color()
        self.background_color = Theme.get_color("background")
        Collections.register("screen", self)

    def prepare(self):
        pass

    def draw(self):
        self.render_surface.fill(self.background_color)

    def update(self, delta_time):
        return None

    def mouse_event(self, event):
        pass

    def key_press(self, event):
        pass

    def set_screen_size(self, screen_size):
        self.screen_size = screen_size

    def reapply_theme(self):
        self.foreground_color = Theme.get_color("foreground")
        self.background_color = Theme.get_color("background")
