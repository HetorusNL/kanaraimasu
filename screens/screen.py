class Screen:
    def __init__(self, render_surface, surface_size):
        self.render_surface = render_surface
        self.surface_size = surface_size
        self.background_color = (255, 255, 255)

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

    def s2r(self, pos):
        # convert screen coordinate/pos to render surface coordinate/pos
        x = pos[0] * self.surface_size[0] / self.screen_size[0]
        y = pos[1] * self.surface_size[1] / self.screen_size[1]
        return (x, y)

    def r2s(self, pos):
        # convert render surface coordinate/pos to screen coordinate/pos
        x = pos[0] * self.screen_size[0] / self.surface_size[0]
        y = pos[1] * self.screen_size[1] / self.surface_size[1]
        return (x, y)
