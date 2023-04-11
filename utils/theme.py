import json

from .settings import Settings


class Theme:
    @classmethod
    def get_color(cls, which="foreground") -> tuple[int, int, int]:
        themes: dict = Settings.get("themes")  # type:ignore
        theme: str = Settings.get("theme")  # type:ignore
        return tuple(themes[theme][which])
