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

    def inside_rect(self, pos, top_left, bot_right):
        # check that pos is within the top_left and bot_right rectanble for x&y
        return all(
            pos[i] >= top_left[i] and pos[i] <= bot_right[i] for i in range(2)
        )

