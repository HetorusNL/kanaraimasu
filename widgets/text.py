from pygame.font import Font

from .widget import Widget


class Text(Widget):
    ALIGN_CENTER = 1
    ALIGN_LEFT_TOP = 2
    ALIGN_RIGHT_TOP = 3
    ALIGN_LEFT_CENTER = 4
    ALIGN_RIGHT_CENTER = 5

    def __init__(
        self,
        surface,
        rect,
        text="",
        color=(0, 0, 0),
        width=10,
        align=ALIGN_CENTER,
    ):
        Widget.__init__(self, surface, rect)
        self.text = text
        self.text_color = color
        self.width = width
        self.font_size = 100
        self.align = align
        self.fonts = {}

    # setters for the properties, they  return self so are chainable
    def set_color(self, color):
        self.set_text_color(color)
        return self

    def set_text_color(self, color):
        self.text_color = color
        return self

    def set_text(self, text):
        self.text = text
        return self

    def set_font_size(self, size):
        self.font_size = size
        return self

    def set_align(self, align):
        self.align = align
        return self

    # basic functions for the widget
    def render(self):
        # draw the text
        self.draw_text()

    def draw_text(self):
        if not self.fonts.get(str(self.font_size)):
            self.fonts[str(self.font_size)] = Font(None, self.font_size)
        font = self.fonts[str(self.font_size)]
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        if self.align == self.ALIGN_LEFT_TOP:
            text_rect.topleft = self.rect.topleft
        elif self.align == self.ALIGN_RIGHT_TOP:
            text_rect.topright = self.rect.topright
        elif self.align == self.ALIGN_LEFT_CENTER:
            text_rect.midleft = self.rect.midleft
        elif self.align == self.ALIGN_RIGHT_CENTER:
            text_rect.midright = self.rect.midright
        else:  # self.ALIGN_CENTER and default
            text_rect.center = self.rect.center
        self.surface.blit(text, text_rect)
