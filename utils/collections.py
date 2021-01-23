from .theme import Theme


class Collections:
    _collections = {}

    @classmethod
    def register(cls, obj_type, obj):
        if not cls._collections.get(obj_type):
            cls._collections[obj_type] = []
        cls._collections[obj_type].append(obj)

    @classmethod
    def reapply_theme(cls):
        foreground_color = Theme.get_color()
        background_color = Theme.get_color("background")
        # process widgets
        for widget in cls._collections.get("widget", []):
            widget.reapply_theme()
        # process screens
        for screen in cls._collections.get("screen", []):
            screen.reapply_theme(foreground_color, background_color)