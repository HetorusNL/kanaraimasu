import json


class Settings:
    defaults = {
        "width": 1280,
        "height": 720,
        "fullscreen": False,
        "fps": 60,
        "stroke_width": 10,
        "dark_theme": False,
        "randomize_kana": True,
        "learn_hiragana": False,
        "learn_katakana": False,
        "hiragana_kana": [],
        "katakana_kana": [],
    }

    @classmethod
    def get(cls, setting, default=None):
        settings = cls.load_settings_file()

        # try to get the setting from the file
        if settings.get(setting) is not None:
            value = settings.get(setting)
        else:
            # otherwise return default value if provided
            if default:
                value = default
            else:
                # otherwise return the value from defaults
                value = cls.defaults.get(setting)

        print(f"[ Settings.get ] {setting}: {value}")
        return value

    @classmethod
    def set(cls, setting, value):
        settings = cls.load_settings_file()
        print(f"[ Setting.set ] {setting}: {value}")
        settings[setting] = value
        cls.store_settings_file(settings)

    @classmethod
    def load_settings_file(cls):
        try:
            # try to open the settings file with fallback to initial values
            with open("settings.json") as f:
                settings = json.load(f)
        except:
            print("failed to open settings file, initial values used!")
            settings = {}

        return settings

    @classmethod
    def store_settings_file(cls, settings):
        with open("settings.json", "w") as f:
            json.dump({**cls.defaults, **settings}, f, indent=2)

