import json


class Settings:
    defaults = {
        "settings_version": 0.1,
        "width": 1280,
        "height": 720,
        "fullscreen": False,
        "fps": 60,
        "stroke_width": 10,
        "randomize_kana": True,
        "learn_hiragana": False,
        "learn_katakana": False,
        "learn_kanji": False,
        "hiragana_kana": [],
        "katakana_kana": [],
        "kanji_show_kun": False,
        "kanji_show_on": False,
        "kanji_show_dutch": False,
        "themes": {
            "dark": {
                "foreground": [255, 255, 255],
                "background": [0, 0, 0],
                "primary": [127, 127, 127],
                "secondary": [50, 50, 50],
                "good": [0, 255, 0],
                "bad": [255, 0, 0],
                "draw": [0, 0, 255],
            },
            "kotatsu": {
                "foreground": [0, 0, 0],
                "background": [247, 237, 227],
                "primary": [255, 116, 92],
                "secondary": [226, 226, 226],
                "good": [0, 230, 118],
                "bad": [255, 87, 34],
                "draw": [0, 0, 0],
            },
            "hetorusnl": {
                "foreground": [255, 255, 255],
                "background": [0, 0, 0],
                "primary": [69, 39, 160],
                "secondary": [26, 26, 26],
                "good": [40, 167, 69],
                "bad": [250, 30, 81],
                "draw": [69, 39, 160],
            },
            "light": {
                "foreground": [0, 0, 0],
                "background": [255, 255, 255],
                "primary": [200, 200, 200],
                "secondary": [200, 200, 200],
                "good": [0, 255, 0],
                "bad": [255, 0, 0],
                "draw": [0, 0, 255],
            },
        },
        "theme": "kotatsu",
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

            settings_version = settings.get("settings_version", 0)
            # if older settings version, make backup and load initial set
            if settings_version < cls.defaults["settings_version"]:
                print(
                    "a new version of the Kanaraimasu settings file "
                    "is available, your settings are reset to default!\n"
                    "(a backup can be found in settings.json.bak)"
                )
                # save the backup
                with open("settings.json.bak", "w") as f_bak:
                    json.dump(settings, f_bak, indent=2)

                # store and load the initial settings
                cls.store_settings_file({})
                with open("settings.json") as f:
                    settings = json.load(f)
        except:
            print("failed to open settings file, initial values used!")
            # store and load the initial settings
            cls.store_settings_file({})
            with open("settings.json") as f:
                settings = json.load(f)

        return settings

    @classmethod
    def store_settings_file(cls, settings):
        with open("settings.json", "w") as f:
            json.dump({**cls.defaults, **settings}, f, indent=2)
