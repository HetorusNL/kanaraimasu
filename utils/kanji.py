import json


class Kanji:
    def __init__(self, dict_name: str) -> None:
        # store the dict_name
        self.dict_name: str = dict_name
        # (re)load the kanji dictionary
        self.reload_kanji()

    def reload_kanji(self) -> None:
        # load the dictionary name
        with open(f"assets/{self.dict_name}", encoding="utf-8") as f:
            self.kanji_dict: list[dict] = json.load(f)
