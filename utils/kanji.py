import json

from .settings import Settings


class Kanji:
    def __init__(self, dict_name):
        # store the dict_name
        self.dict_name = dict_name
        # (re)load the kanji dictionary
        self.reload_kanji()

    def reload_kanji(self):
        # load the dictionary name
        with open(f"assets/{self.dict_name}", encoding="utf-8") as f:
            self.kanji_dict = json.load(f)
