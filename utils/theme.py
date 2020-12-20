import json

from .settings import Settings


class Theme:
    @classmethod
    def get_color(cls, which="foreground"):
        themes = Settings.get("themes")
        theme = Settings.get("theme")
        return tuple(themes[theme][which])
